from django.contrib import admin
from django.urls import path
from . import views

app_name = 'birds'

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='order-list'),
    path('locations/', views.location_list, name='order-list'),
    path('events/', views.event_list, name='event-list'),
    path('events/<int:year>/<int:month>/', views.event_list, name='event-list'),
    path('all-birds/', views.all_birds, name='all-birds'),
    path('order/<slug:order_slug>/', views.order_detail, name="order-detail"),
    path('family/<slug:family_slug>/', views.family_detail, name="family-detail"),
    path('genus/<slug:genus_slug>/', views.genus_detail, name="genus-detail"),
    path('species/<slug:species_slug>/', views.species_detail, name="species-detail"),
    path('location/<slug:location_slug>/', views.location_detail, name="location-detail"),
    path('event/<slug:event_slug>/', views.event_detail, name="event-detail"),
]