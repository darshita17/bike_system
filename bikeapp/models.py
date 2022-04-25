from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from PIL import Image

class Bike(models.Model):
    bike_name=models.CharField(max_length=255)
    description=models.TextField()
    brand=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.CharField(max_length=255)
    image=models.ImageField(default='/profile_pics/default.jpg',upload_to='profile_pics')
    complete=models.BooleanField(default=False)

    def __str__(self):
        return self.bike_name
    @property
    def hourly_prices(self):
        h=self.price
        h=h*5
        return h

    @property
    def daily_prices(self):
        h=self.price
        h=h*20
        return h

    @property
    def weekly_prices(self):
        h=self.price
        h=h*60
        return h

class common(models.Model):
    start_date=models.DateField()
    end_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()


class Location(models.Model):
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    area=models.CharField(max_length=50)

    def __str__(self):
        return self.city

class Booking(common):
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='/default.jpg',upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username}Profile'

    def save(self):
        super().save()

        img=Image.open(self.image.path)

        if img.height >300 or img.width >300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Cart(common):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike,on_delete=models.CASCADE)
    total_price=models.FloatField()
    discount_price=models.FloatField()

class CalcTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike,on_delete=models.CASCADE)
    timing=models.CharField(max_length=50)


