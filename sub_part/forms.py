from typing import Any
from django import forms
from sub_part.models import *

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id',)
   
    # project_name = forms.CharField(label='Project Name', max_length=100)
    # location = forms.CharField(label='Location', max_length=100)
    def __init__(self, *args, **kwargs):
        super(ProjectCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ScreenForm(forms.Form):
    table_name = forms.CharField(max_length=100)
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label='Project')


    def __init__(self, *args, **kwargs):
            super(ScreenForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

class ScreenElementForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    class Meta:
        model = Screen
        fields = ('id', 'screen_name', 'project')
        read_only_fields = ('id',)
      
    def __init__(self, *args, **kwargs):
            super(ScreenElementForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

class TableForm(forms.ModelForm):
    class Meta:
        model=Table
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ('id',)
    # field_name = forms.CharField()
    # field_type = forms.CharField()
    # max_length = forms.IntegerField(required=False)
    # required = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ArgumentForm(forms.ModelForm):
    class Meta:
        model=Argument
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(ArgumentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class ViewForm(forms.ModelForm):
    class Meta:
        model=View
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class FormForm(forms.ModelForm):
    class Meta:
        model=Form
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(FormForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AlertForm(forms.ModelForm):
    class Meta:
        model=Alert
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class A_ButtonForm(forms.ModelForm):
    class Meta:
        model=A_Button
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(A_ButtonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ButtonForm(forms.ModelForm):
    class Meta:
        model=Button
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(ButtonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class CardForm(forms.ModelForm):
    class Meta:
        model=Card
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DropdownForm(forms.ModelForm):
    class Meta:
        model=Dropdown
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(DropdownForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class InputForm(forms.ModelForm):
    class Meta:
        model=Input
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ModalForm(forms.ModelForm):
    class Meta:
        model=Modal
        fields=['modal_description']

    def __init__(self, *args, **kwargs):
        super(ModalForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class FormWidgetForm(forms.ModelForm):
    class Meta:
        model=FormWidget
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(FormWidgetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Select an Excel file',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'padding-top: 5px;'})
    )

from ckeditor.widgets import CKEditorWidget

class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = ['description']
        widgets = {
            'description': CKEditorWidget(),
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model=Menu
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class MainSubMenuForm(forms.ModelForm):
    class Meta:
        model=MainSubMenu
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(MainSubMenuForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SubMenuForm(forms.ModelForm):
    class Meta:
        model=SubMenu
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(SubMenuForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            
class IconMasterForm(forms.ModelForm):
    class Meta:
        model=IconMaster
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(IconMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class YourForm(forms.Form):
    selected_screen_id = forms.IntegerField(required=False, widget=forms.HiddenInput())


class UserTypeMasterForm(forms.ModelForm):
    class Meta:
        model=UserTypeMaster
        exclude=('project',)

    def __init__(self, *args, **kwargs):
        super(UserTypeMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'