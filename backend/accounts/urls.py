from django.urls import path
from .views import (
    RegisterView, VerifyEmailView, MeView,
    AdminUserListCreateView, AdminUserRetrieveUpdateDestroyView,
    UserRetrieveUpdateView, SendPhoneOtpView, VerifyPhoneOtpView
)
from .authentication import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .password_views import PasswordResetRequestAPIView, PasswordResetConfirmAPIView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),

    path("users/", AdminUserListCreateView.as_view(), name="admin-users"),
    path("users/<int:pk>/", AdminUserRetrieveUpdateDestroyView.as_view(), name="admin-user-detail"),

    path("profile/", UserRetrieveUpdateView.as_view(), name="profile"),

    path("phone/send-otp/", SendPhoneOtpView.as_view(), name="send-otp"),
    path("phone/verify-otp/", VerifyPhoneOtpView.as_view(), name="verify-otp"),

    path("password/reset/", PasswordResetRequestAPIView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmAPIView.as_view(), name="password_reset_confirm"),
]
