from rest_framework import serializers
from .models import *

class UserTypeMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserTypeMaster
		fields = "__all__"

class ScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Screen
		fields = "__all__"
		
class ScreenVersionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScreenVersion
		fields = "__all__"

class ScreenVersionFieldsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScreenVersionFields
		fields = "__all__"
