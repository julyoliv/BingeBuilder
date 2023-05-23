from django.urls import path
from . import views

urlpatterns = [
    path('my_certificates/', views.my_certificates, name="my_certificates"),
]