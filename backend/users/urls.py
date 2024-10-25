from django.urls import path
from .views import UserRegistrationView, EmailVerificationView, SelectWinnerView, UserListView, SetPasswordView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='verify_email'),
    path('winner/', SelectWinnerView.as_view(), name='select_winner'),
    path('list/', UserListView.as_view(), name='user_list'), 
    path('set-password/', SetPasswordView.as_view(), name='set_password'),
]
