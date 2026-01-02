from django.db import models

from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    



import uuid
import qrcode
from io import BytesIO
from django.core.files import File

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def generate_qr(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.code)
        qr.make()

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_image.save(f'{self.code}.png', File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())

        if not self.qr_image:  # Generate QR only on first save
            self.generate_qr()

        super().save(*args, **kwargs)




# Create your models here.
