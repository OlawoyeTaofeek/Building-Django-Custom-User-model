from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
     path('', views.welcome, name='welcome'),
     path('login/', views.login, name='login'),
     path('register/', views.register, name='register')
]