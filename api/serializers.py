from rest_framework import serializers, fields
from sub_part.models import Table
from sub_part.models import *


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
