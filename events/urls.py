from django.urls import path
from .views import RegisterView,EventListCreateView,BookingCreateView,CreateCheckoutSessionView, ConfirmPaymentView
from rest_framework_simplejwt.views import TokenObtainPairView




urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('events/',EventListCreateView.as_view()),
    path('book/', BookingCreateView.as_view()),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('confirm-payment/', ConfirmPaymentView.as_view()),



]
