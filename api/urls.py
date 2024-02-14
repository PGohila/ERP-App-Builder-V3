from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .models import*

urlpatterns = [

path('table', views.TableView.as_view(), name='table_api'),
path('table_update/<int:pk>/', views.TableChangeView.as_view(), name='table_update'),

]

