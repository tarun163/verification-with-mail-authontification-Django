
from django.contrib import admin
from django.urls import path,include
from home import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('token/',views.token_send, name='token_send'),
    path('success/',views.success,name="success"),
    path('verify/<auth_token>',views.verify, name="verify"),
     path('reset_verify/<auth_token>',views.reset_verify, name="reset_verify"),
    path('error',views.error_page,name="error"),
    path('forget_password',views.forget_password,name="forget_password"),
    path('reset_password',views.reset_password,name="reset_password")
]
