from django.shortcuts import render,redirect,get_object_or_404


from django.views.generic import ListView, UpdateView, CreateView, DetailView
from .models import *
from .api_call import call_post_method_without_token_app_builder,call_get_method,call_get_method_without_token,call_post_with_method,call_post_method_for_without_token,call_delete_method,call_delete_method_without_token, call_put_method,call_put_method_without_token
import requests
import json
from django.contrib import messages
from django.urls import resolve, reverse
import jwt
from django.contrib.auth import logout
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib import messages
from django.conf import settings
BASE_URL = 'http://127.0.0.1:2222/'
APP_BUILDER = 'http://127.0.0.1:8000/'

def dashboard(request):

    return render(request, 'dashboard.html')

class SetupView(APIView):
    def get(self, request):
        records = UserTypeMaster.objects.all()
        serializer = UserTypeMasterSerializer(records, many=True)
        return Response(serializer.data)
    def post(self, request):   
        serializer =  request.data # DATA STURCTURE Come like [{},{}]
        for data in serializer: 
            if data == "usertype":
                for data1 in request.data["usertype"]:
                    serializer = UserTypeMasterSerializer(data = data1)
                    if serializer.is_valid():
                        print("usertype data saved")
                        serializer.save()
                    else:
                        print("error",serializer.errors)
            elif data == "screentable":
                for data1 in request.data["screentable"]:
                    serializer = ScreenSerializer(data = data1)
                    if serializer.is_valid():
                        print("screen data saved")
                        serializer.save()
                    else:
                        print("error",serializer.errors)
            elif data == "screenversion":
                for data1 in request.data["screenversion"]:
                    serializer = ScreenVersionSerializer(data = data1)
                    if serializer.is_valid():
                        print("screen version data saved")
                        serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)