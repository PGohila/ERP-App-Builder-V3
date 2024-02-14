from import_export import resources
from .models import *

class TableResource(resources.ModelResource):
    class Meta:
        model = Table
       

class FieldResource(resources.ModelResource):
    class Meta:
        model = Field
       

class ScreenResource(resources.ModelResource):
    class Meta:
        model = Screen
       

class ArgumentResource(resources.ModelResource):
    class Meta:
        model = Argument
       

class FormResource(resources.ModelResource):
    class Meta:
        model = Form

class WidgetResource(resources.ModelResource):
    class Meta:
        model = Widget

class AlertResource(resources.ModelResource):
    class Meta:
        model = Alert

class A_ButtonResource(resources.ModelResource):
    class Meta:
        model = A_Button

class ButtonResource(resources.ModelResource):
    class Meta:
        model = Button

class CardResource(resources.ModelResource):
    class Meta:
        model = Card

class DropdownResource(resources.ModelResource):
    class Meta:
        model = Dropdown

class InputResource(resources.ModelResource):
    class Meta:
        model = Input

class ModalResource(resources.ModelResource):
    class Meta:
        model = Modal

class FormWidgetResource(resources.ModelResource):
    class Meta:
        model = FormWidget

class CardImagesResource(resources.ModelResource):
    class Meta:
        model = CardImages

class MenuResource(resources.ModelResource):
    class Meta:
        model = Menu

class MainSubMenuResource(resources.ModelResource):
    class Meta:
        model = MainSubMenu

class SubMenuResource(resources.ModelResource):
    class Meta:
        model = Menu

class IconMasterResource(resources.ModelResource):
    class Meta:
        model = IconMaster

class CheckboxResource(resources.ModelResource):
    class Meta:
        model = Checkbox

class FieldSizeResource(resources.ModelResource):
    class Meta:
        model = FieldSize

class UserTypeMasterResource(resources.ModelResource):
    class Meta:
        model = UserTypeMaster

