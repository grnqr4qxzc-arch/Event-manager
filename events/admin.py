from django.contrib import admin
from .models import Event, Booking, Ticket

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'price', 'created_by', 'created_at')
    list_filter = ('location', 'date')
    search_fields = ('title', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'total_price', 'created_at')
    list_filter = ('event', 'user')
    search_fields = ('user__username', 'event__title')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'booking', 'is_used')
    list_filter = ('is_used',)
    search_fields = ('code',)


# Register your models here.
