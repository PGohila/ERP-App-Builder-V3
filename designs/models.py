from django.core.validators import MinValueValidator,FileExtensionValidator,MaxValueValidator
from django.db import models

class Screen(models.Model):
    screen_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.screen_name 
    
class UserTypeMaster(models.Model):
    user_type=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self) -> str:
        return self.user_type
    
class ScreenVersion(models.Model):
    verion_name=models.CharField(max_length=50)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserTypeMaster, on_delete=models.CASCADE)
    status=models.CharField(max_length=10, default="pending")
    def __str__(self) -> str:
        return self.verion_name
    
class ScreenVersionFields(models.Model):
    version = models.ForeignKey(ScreenVersion, on_delete=models.CASCADE)
    field = models.CharField(max_length=50, blank=True,null=True)
    column_size = models.IntegerField()
    label_name = models.CharField(max_length=50, blank=True,null=True)
    position = models.IntegerField(blank=True, null=True)

class Table1(models.Model):
	field1 = models.CharField(max_length=10, blank=True, null=True, help_text="only text")
