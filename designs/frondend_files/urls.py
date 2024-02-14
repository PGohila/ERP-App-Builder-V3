from django.urls import path

from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('setup', setup, name='setup'),
]