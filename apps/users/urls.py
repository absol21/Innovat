from django.urls import path, include
# from .views import google_login, google_auth
from .views import (
        ChangePasswordView,
        ForgotPasswordView,
        ForgotPasswordCompleteView, 
        RegisterView, 
        ActivationView, 
        EditProfileView, 
        EditAvatarView,
        MyProfileAPIView,
        ProfileView,
        RatingViewApi
    )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('edit_profile/', EditProfileView.as_view(), name='edit-profile'),
    path('edit_avatar/', EditAvatarView.as_view(), name='edit-avatar'),
    path('userpage/', MyProfileAPIView.as_view(), name='profile-list'),
    path('userpage/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('ratings/', RatingViewApi.as_view(), name='ratings'),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view(), name='forgot_password_complete'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
]


