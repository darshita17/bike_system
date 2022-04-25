from django.contrib import admin
from .models import *

@admin.register(Bike)
class BikeModelAdmin(admin.ModelAdmin):
	list_display=['id','bike_name','description','brand','price','capacity','image','complete']

# admin.site.register(Booking)
@admin.register(Booking)
class BookingModelAdmin(admin.ModelAdmin):
	list_display=['id','location','user','start_date','end_date','start_time','end_time']

@admin.register(Location)
class LocationModelAdmin(admin.ModelAdmin):
	list_display=['id','city','state','area']

@admin.register(Profile)
class LocationModelAdmin(admin.ModelAdmin):
	list_display=['id','user','image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display=['id','total_price','discount_price','bike_id','user_id','start_date','end_date','start_time','end_time']

@admin.register(CalcTime)
class CalcTimeModelAdmin(admin.ModelAdmin):
	list_display=['id','user','bike','timing']