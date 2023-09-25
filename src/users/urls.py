from django.urls import path

from .views import RegisterView, SendOTPView,VerifyOTP,LoginRequiredView, LogoutAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('sendotp/',SendOTPView.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('requiredlogin/', LoginRequiredView.as_view()),
    path('logout/', LogoutAPIView.as_view()),

]