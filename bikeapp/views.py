# Create your views here.
from . filter import *
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . forms import CustomerRegistrationForm ,ProfileUpadateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Bike,Booking,Location,Cart,CalcTime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
# from requests import Request, Session
from django.http import JsonResponse
import requests
from django.contrib import messages

# def home(request):
#     if request.method=="POST":
#         data={
#         "pickuplocation":request.POST['pickuplocation'],
#         "pickupdate":request.POST['pickupdate'],
#         "dropoffdate":request.POST['dropoffdate'],
#         "pickuptime":request.POST['pickuptime'],
#         "droptime":request.POST['droptime'],
#         }
#         print(data,"lll")

#         print(data["droptime"])

#         start_date_change=data["pickupdate"]
#         # print(start_date_change,"'llljjj")

#         start_dates=datetime.datetime.strptime(start_date_change, '%m/%d/%Y').strftime('%Y-%m-%d')
#         # print(start_dates,"nnnn")

#         end_date_change=data["dropoffdate"]

#         end_dates=datetime.datetime.strptime(end_date_change, '%m/%d/%Y').strftime('%Y-%m-%d')
#         # print(end_dates,"nnnn")

#         book=Booking.objects.filter(location__city=data["pickuplocation"],start_date=start_dates,end_date=end_dates,start_time=data["pickuptime"],end_time=data["droptime"])
    
#         context={
#             "data":data
#             }
#         return redirect('showbike')

#         respose=render(request,'bikeapp/home.html',context)
#         respose.set_cookie('pickuplocation',context)
#         return respose
# def home(request):

def get_topics_ajax(request):
    if request.method == "POST":
        subject_id = request.POST['subject_id']
        bike_id = request.POST['bike_id']
        price=Bike.objects.get(id=bike_id)
        try:
            hourly_charge=daily_charge=weekly_charge= 0
            if subject_id=="h":
                hourly_charge=price.price
                hourly_charge=hourly_charge*5
                print("Hourl",hourly_charge)

            if subject_id=="d":
                daily_charge=price.price
                daily_charge=daily_charge*20
                print("Hourl",daily_charge)

            if subject_id=="w":
                weekly_charge=price.price
                weekly_charge=weekly_charge*60
                print("Hourl",weekly_charge)

        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse((hourly_charge,daily_charge,weekly_charge), safe = False)

def home(request):
    if request.method=="POST":
        data={
        "pickuplocation":request.POST['pickuplocation'],
        "pickupdate":request.POST['pickupdate'],
        "dropoffdate":request.POST['dropoffdate'],
        "pickuptime":request.POST['pickuptime'],
        "droptime":request.POST['droptime'],
        }
        response=redirect('showbike')
        response.set_cookie(key='pickuplocation',value=data["pickuplocation"])
        response.set_cookie(key='pickupdate',value=data["pickupdate"])
        response.set_cookie(key='dropoffdate',value=data["dropoffdate"])
        response.set_cookie(key='pickuptime',value=data["pickuptime"])
        response.set_cookie(key='droptime',value=data["droptime"])

        return response
    elif request.method=="GET":
        return render(request,"bikeapp/home.html")

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'bikeapp/register.html',{'form':form})

    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations...!! register Successfully')
            form.save()
            return redirect('login')        
        return render(request,'bikeapp/register.html',{'form':form})

def get_bike(request):
        context={}
        bike=Bike.objects.filter(complete=False)
        filter_bike = BikeFilter(request.GET, queryset=bike) 
        context['filter_bike']=filter_bike
        return render(request,"bikeapp/car.html",context=context)

def book_bike(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        bid=Bike.objects.get(pk=pk)
        print(bid.complete,"mmmm")
        user=request.user
        location=request.COOKIES.get("pickuplocation")
        pickupdate=request.COOKIES.get("pickupdate")
        dropoffdate=request.COOKIES.get("dropoffdate")
        pickuptime=request.COOKIES.get("pickuptime")
        droptime=request.COOKIES.get("droptime")
        
        if request.method=='POST':
            user_id=request.user.id
            state=request.POST.get('state')
            city=request.POST.get('city')
            area=request.POST.get('area')
            print(state,"lll")
            pickdate=pickupdate

            dropdate=dropoffdate
            pickuptime=pickuptime
            droptime=droptime

            data=Location(city=city,state=state,area=area)
            data.save()

            book = Booking(location=data,user=user,start_date=pickdate,end_date=dropdate,start_time=pickuptime,end_time=droptime)
            book.save()

            bid.complete=True
            bid.save()
        return render(request,"bikeapp/booking.html",{"bike":bid,"user":user,"location":location,"pickupdate":pickupdate,"dropoffdate":dropoffdate,"pickuptime":pickuptime,"droptime":droptime})

def get_bike_details(request,pk):
    bike=Bike.objects.get(pk=pk)
    print(bike.id,"mmmmmmm")
    user=request.user
    booking_data=Booking.objects.filter(pk=pk)
    print(booking_data,"kkknnnnnk")

    # print(booking_data,"nnnn")
    
    # for i in booking_data:
    #     s_date=i.start_date
    #     e_date=i.end_date
    #     s_time=i.start_time
    #     e_time=i.end_time

    # a=e_date-s_date
    # print(a,"kk")

    # b=datetime(1970,1,1,s_time.hour,s_time.minute,s_time.minute)
    # c=datetime(1970,1,1,e_time.hour,e_time.minute,e_time.minute)

    # d=b-c
    # print(d)

    if request.method=="POST":
        val=request.POST.get('get_val')
        print(val,"__________________________")

        cart=CalcTime(user=user,bike=bike,timing=val)
        cart.save()
        return redirect('cart',pk=pk)
    return render(request,"bikeapp/bike_details.html",{'bike':bike})

def profile(request):
    if request.method=='GET':
        user=request.user
        u_form=CustomerRegistrationForm(instance=request.user)
        p_form=ProfileUpadateForm(instance=request.user)

        context={
            'p_form':p_form,
            'u_form':u_form
        }
        return render(request,'bikeapp/myprofile.html',context)

def bike_filter(request):
    return render(request,'bikeapp/car.html')

def cart(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        bike_details=[]
        user=request.user
        user_id=request.user.id
        bike_data=Bike.objects.get(pk=pk)

        booking_data=Booking.objects.filter(user=user)
        pickupdate=request.COOKIES.get("pickupdate")
        dropoffdate=request.COOKIES.get("dropoffdate")
        pickuptime=request.COOKIES.get("pickuptime")
        droptime=request.COOKIES.get("droptime")
        
        s=Cart(user=user,bike=bike_data,total_price="100",discount_price="90",start_date=pickupdate,start_time=pickuptime,end_date=dropoffdate,end_time=droptime)
        s.save()

        get_bike=list(Cart.objects.filter(user=user))
        print(get_bike,"vbbnnnn")
        
        for i in get_bike:
            print(i.bike_id) 
            p1 = Bike.objects.get(pk=i.bike.id)  
            bike_details.append(p1) 
        
        context={
        "bike":bike_details,
        "booking":get_bike
        }

        x=zip(bike_details,get_bike)
        return render(request,"bikeapp/cart.html",{"bike":bike_details,"booking":get_bike,"x":x})

def ab(request):
    if request.method=="POST":
        val=request.POST.get('get_val')
        print(val,"__________________________")

    return render(request,"bikeapp/ab.html")


def delete_cart(request,pk): 
    cart_data =get_object_or_404(Cart,common_ptr_id=pk)
    print(cart_data,"nnn")
    cart_data.delete()
    print(cart_data,"nnnbbb")
    messages.success(request,f'Deleted Succesfully....!!!')
    return redirect("cart",pk=cart_data.bike_id)
    

