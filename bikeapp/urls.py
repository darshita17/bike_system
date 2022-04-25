from django.contrib import admin
from django.urls import path
from bikeapp import views
from django.contrib.auth import views as auth_views
from . forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bikeapp/login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"),name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='bikeapp/passwordchange.html',form_class=MyPasswordChangeForm,success_url="/passwordchangedone"),name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='bikeapp/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='bikeapp/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='bikeapp/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='bikeapp/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='bikeapp/password_reset_complete.html'),name='password_reset_complete'),
    path('register/', views.CustomerRegistrationView.as_view(),name='register'),
    path('myprofile/',views.profile,name='myprofile'),
    path('bike/',views.get_bike,name='showbike'),
    path('bike-detail/<int:pk>',views.get_bike_details,name="bikedetails"),
    path('bookbike/<int:pk>',views.book_bike,name="bookbike"),
    path('get-topics-ajax/', views.get_topics_ajax, name="get_topics_ajax"),
    path('cart/<int:pk>', views.cart, name="cart"),
    path('ab', views.ab, name="ab"),
    path('deletecart/<int:pk>',views.delete_cart,name="deletecart")
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)