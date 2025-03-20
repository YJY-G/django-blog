from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<slug:slug>', views.details, name='details'),
]
