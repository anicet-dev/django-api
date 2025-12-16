from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()

class PasswordResetRequestAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail":"Email requis."}, status=400)
        form = PasswordResetForm({"email": email})
        if form.is_valid():
            form.save(
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                request=request
            )
        return Response({"detail":"Si un compte existe, un email a été envoyé."})

class PasswordResetConfirmAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("password")
        if not uidb64 or not token or not new_password:
            return Response({"detail":"Paramètres manquants."}, status=400)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail":"Lien invalide."}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({"detail":"Token invalide ou expiré."}, status=400)
        form = SetPasswordForm(user, {"new_password1": new_password, "new_password2": new_password})
        if form.is_valid():
            form.save()
            return Response({"detail":"Mot de passe mis à jour."})
        return Response(form.errors, status=400)
