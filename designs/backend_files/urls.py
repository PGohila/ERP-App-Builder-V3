from django.urls import path

from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path("set_up", SetupView.as_view(), name='setup'),

]