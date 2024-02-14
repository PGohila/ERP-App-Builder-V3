from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from sub_part.models import *

# Create your views here.

from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from sub_part.models import Table

from .serializers import (
Table
)
from drf_yasg.utils import swagger_auto_schema


from .serializers import *

from django.contrib.auth.hashers import make_password


class TableView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TableSerializer

    @swagger_auto_schema(responses={200: TableSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        table= Table.objects.all()
        serializer = TableSerializer( table, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=TableSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = TableSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TableChangeView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TableSerializer

    @swagger_auto_schema(responses={200: TableSerializer})
    def get(self, request,pk, format=None, *args, **kwargs):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TableSerializer)
    def put(self, request, pk, format=None, *args, **kwargs):
        table = get_object_or_404(Table, pk=pk)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None, *args, **kwargs):
        table = get_object_or_404(Table, pk=pk)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)