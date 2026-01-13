
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer,MyTicketSerializer
from .models import Ticket,Booking
from decimal import Decimal

import stripe
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)
    
    
    



class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)





class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event_id')
        quantity = int(request.data.get('quantity', 1))

        # Validate event
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)

        # Calculate total price
        total_price = Decimal(event.price) * quantity
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            quantity=quantity,
            total_price=total_price
        )

        # Create tickets
        for _ in range(quantity):
            Ticket.objects.create(booking=booking)

        return Response({
            "message": "Booking successful",
            "booking_id": booking.id,
            "total_price": total_price,
            "tickets": [t.code for t in booking.ticket_set.all()]
        }, status=201)



stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        event_id = request.data.get("event_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        # Create booking (unpaid for now)
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            quantity=quantity,
            total_price=event.price * quantity,
            is_paid=False
        )

        # Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': event.title,
                    },
                    'unit_amount': int(event.price * 100),  # in paise
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=f"{settings.STRIPE_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}",
            cancel_url=settings.STRIPE_CANCEL_URL,
            metadata={"booking_id": booking.id}
        )

        return Response({
            "checkout_url": session.url
        }, status=200)
    


class ConfirmPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        booking_id = request.data.get("booking_id")

        # Fetch Stripe session details
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            return Response({"error": "Payment not completed"}, status=400)

        # Fetch booking
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        # Mark booking as paid
        booking.is_paid = True
        booking.save()

        # Generate tickets
        for _ in range(booking.quantity):
            Ticket.objects.create(booking=booking)

        return Response({
            "message": "Payment confirmed & tickets generated",
            "booking_id": booking.id,
            "tickets": [t.code for t in booking.ticket_set.all()]
        }, status=200)





class ValidateTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ticket_code = request.data.get("ticket_code")

        if not ticket_code:
            return Response(
                {"error": "Ticket code is required"},
                status=400
            )

        try:
            ticket = Ticket.objects.get(code=ticket_code)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Invalid ticket"},
                status=404
            )

        if ticket.is_used:
            return Response(
                {"error": "Ticket already used"},
                status=400
            )

        # Mark ticket as used
        ticket.is_used = True
        ticket.save()

        return Response({
            "message": "Ticket validated successfully",
            "event": ticket.booking.event.title,
            "user": ticket.booking.user.username
        }, status=200)
    



class MyTicketsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(booking__user=request.user)
        serializer = MyTicketSerializer(tickets, many=True)
        return Response(serializer.data, status=200)

