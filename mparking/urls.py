from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('entry/', views.entry, name='entry'),
    path('exit/', views.exit, name='exit'),
    path('slots/', views.slots, name='slots'),
    path('dashboard/', views.dashboard, name='dashboard'),
]