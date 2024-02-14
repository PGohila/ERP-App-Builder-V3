from django.shortcuts import render,redirect,get_object_or_404


from django.views.generic import ListView, UpdateView, CreateView, DetailView

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
from .forms import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib import messages
from django.conf import settings
BASE_URL = 'http://127.0.0.1:2222/'
APP_BUILDER = 'http://127.0.0.1:8000/'

def dashboard(request):

    return render(request, 'dashboard.html')

def setup(request):
    endpoint = 'project_setups/'
    endpoint1 = 'set_up'
    json_data = settings.PROJECT_ID # value is 32
    json_data = {"project_id": settings.PROJECT_ID}
    json_body = json.dumps(json_data)
    appbuilder_response = call_post_method_for_without_token(APP_BUILDER,endpoint,json_body)
    if appbuilder_response.status_code == 201:
        #save all usertype and other table data to new project 
        dic = {}
        records1 = appbuilder_response.json() # all table data structure is [ [{table1},{}],[{table2},{}] ]
        for index,data in enumerate(records1):
            if index == 0:
                dic["usertype"] = data
            elif index == 1:
                dic["screentable"] = data
            elif index == 2:
                dic["screenversion"] = data  

        alltable_data = json.dumps(dic)
        response1 = call_post_method_for_without_token(BASE_URL, endpoint1, alltable_data)
        if response1.status_code == 201:
            messages.success(request,'Your System Successfully Setup', extra_tags="success")
        else:
            print("error",response1.json())
            # return redirect('setup')    
    else:
        print("error")
    
    return redirect("dashboard")
