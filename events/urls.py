from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('new_marathon/', views.new_marathon, name="new_marathon"),
    path('manage_marathon/', views.manage_marathon, name="manage_marathon"),
    path('register_marathon/<int:id>/', views.register_marathon, name="register_marathon"),
    path('users_event/<int:id>/', views.users_event, name="users_event"),
    path('generate_csv/<int:id>/', views.generate_csv, name="generate_csv"),
    path('certificate_event/<int:id>/', views.certificate_event, name="certificate_event"),
    path('generate_certificate/<int:id>/', views.generate_certificate, name="generate_certificate"),
    path('search_certificate/<int:id>', views.search_certificate, name="search_certificate"),
]