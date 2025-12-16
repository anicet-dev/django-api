from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import random
from .serializers import RegisterSerializer, UserSerializer, AdminUserSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin
from .authentication import MyTokenObtainPairView
from .utils_sms import send_sms

User = get_user_model()
signer = TimestampSigner()

# Endpoint racine API
class RootApiView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({"message": "Bienvenue sur l'API REST !"})

# Inscription et vérification email
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def perform_create(self, serializer):
        user = serializer.save()
        token = signer.sign(user.pk)
        verify_url = self.request.build_absolute_uri(reverse("accounts:verify-email") + f"?token={token}")
        subject = "Vérifiez votre adresse e-mail"
        message = f"Bonjour {user.username},\nCliquez sur le lien pour vérifier votre e-mail : {verify_url}\nLe lien expire dans 24h."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({"detail":"Token manquant."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            unsigned = signer.unsign(token, max_age=60*60*24)
            user = User.objects.get(pk=unsigned)
            user.is_verified = True
            user.save()
            return Response({"detail":"Email vérifié."})
        except SignatureExpired:
            return Response({"detail":"Le lien a expiré."}, status=status.HTTP_400_BAD_REQUEST)
        except (BadSignature, User.DoesNotExist):
            return Response({"detail":"Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

# Profil utilisateur
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# Admin
class AdminUserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer

class AdminUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer

# Owner
class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self):
        return self.request.user

# OTP
class SendPhoneOtpView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        if not user.phone:
            return Response({"detail":"Aucun numéro enregistré."}, status=400)
        code = f"{random.randint(100000,999999)}"
        user.set_otp(code)
        send_sms(user.phone, f"Votre code: {code}")
        return Response({"detail":"OTP envoyé."})

class VerifyPhoneOtpView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"detail":"Code requis."}, status=400)
        user = request.user
        if user.otp_valid(code):
            user.is_verified = True
            user.clear_otp()
            user.save()
            return Response({"detail":"Téléphone vérifié."})
        return Response({"detail":"Code invalide ou expiré."}, status=400)
