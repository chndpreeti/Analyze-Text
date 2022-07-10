
from django.contrib import admin
from django.urls import path
from Analyze import views

urlpatterns = [
    path("", views.index, name='home'),
    path("result", views.result, name='result'),
    path("keyy", views.keyy, name='keyy'),
    path("entity", views.entity, name='entity')
]
