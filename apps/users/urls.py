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
        RatingView
    )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ratings', RatingView)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('edit_profile/', EditProfileView.as_view()),
    path('edit_avatar/', EditAvatarView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view(), name='forgot_password_complete'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('', include(router.urls)),
    # path('google/', google_auth),
    # path('', google_login),
]


