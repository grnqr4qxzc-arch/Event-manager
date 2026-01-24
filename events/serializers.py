from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Event

from .models import Booking,Ticket

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['created_by']

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None




from .models import Booking,Ticket

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price']



class MyTicketSerializer(serializers.ModelSerializer):
    event = serializers.CharField(source='booking.event.title')
    qr_image = serializers.ImageField()

    class Meta:
        model = Ticket
        fields = ['code', 'event', 'qr_image', 'is_used']

