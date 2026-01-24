from django.urls import path
from .views import RegisterView,EventListCreateView,BookingCreateView,CreateCheckoutSessionView, ConfirmPaymentView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import ValidateTicketView,MyTicketsView,EventDetailView




urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('events/',EventListCreateView.as_view()),
    path('book/', BookingCreateView.as_view()),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('confirm-payment/', ConfirmPaymentView.as_view()),
    path('validate-ticket/', ValidateTicketView.as_view()),
    path('my-tickets/', MyTicketsView.as_view()),
    path("events/<int:pk>/", EventDetailView.as_view()),






]
