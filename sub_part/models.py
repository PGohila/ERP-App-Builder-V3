from django.db import models
from ckeditor.fields import RichTextField

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.project_name

class Screen(models.Model):
    screen_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self) -> str:
        return self.screen_name
    
class Table(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Field(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100, null=True, blank=True)
    required = models.CharField(max_length=100, null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    help_text = models.CharField(max_length=100, null=True, blank=True)
    date_format = models.CharField(max_length=100, null=True, blank=True)
    boolean_checkbox = models.BooleanField(default=False,null=True, blank=True)# bool field
    auto_now_checkbox = models.BooleanField(default=False,null=True, blank=True) # Date field
    max_digits = models.IntegerField(null=True, blank=True)
    decimal_places = models.IntegerField(null=True, blank=True)
    file_limit = models.IntegerField(null=True, blank=True)
    table_name = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='Table_name_field',null=True, blank=True) #forignkey
    ip_protocol = models.CharField(max_length=100, null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    min_length = models.IntegerField(null=True, blank=True) #integer field
    many_to_many = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='mamy_to_many_field',null=True, blank=True)
    one_to_one = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='one_to_one_field',null=True, blank=True)
    use_seconds_checkbox = models.BooleanField(default=False,null=True, blank=True)

    def __str__(self) -> str:
        return self.field_name


class Argument(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class View(models.Model):
    METHOD_CHOICES = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
    )
    name = models.CharField(max_length=150)
    args = models.ForeignKey(Argument, help_text="*args", on_delete=models.CASCADE, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default="GET")

    def __str__(self):
        return self.name


class Form(models.Model):
    name = models.CharField(max_length=150)
    fields = models.ForeignKey(Field, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Widget(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    widget_type = models.CharField(max_length=20)
    properties = models.JSONField()

COLOR_CHOICES = [
    ('primary', 'Blue'),
    ('secondary', 'Grey'),
    ('success', 'Green'),
    ('danger', 'Red'),
    ('warning', 'Orange'),
    ('info', 'SkyBlue'),
    ('light', 'Light'),
    ('dark', 'Dark'),
]
# ============ For Widgets =========
class Alert(models.Model):	
    screen_name = models.ForeignKey(Screen, on_delete=models.CASCADE)
    color_code = models.CharField(max_length=20, choices=COLOR_CHOICES)
    message = models.CharField(max_length=250)

    def __str__(self):
         return self.message

class A_Button(models.Model):	
    screen_name = models.ForeignKey(Screen, on_delete=models.CASCADE)
    url_link = models.CharField(max_length=250)
    color_code = models.CharField(max_length=20, choices=COLOR_CHOICES)
    button_name = models.CharField(max_length=50)

class Button(models.Model):	
	BUTTON_TYPES = [
    ('button', 'Button'),
    ('submit', 'Submit'),
	]
	screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
	button_type= models.CharField(max_length=20, choices=BUTTON_TYPES)
	color_code= models.CharField(max_length=20, choices=COLOR_CHOICES)
	button_name= models.CharField(max_length=50)

class Card(models.Model):	
    screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
    size_in_number=models.IntegerField(default='12',help_text="Use number from 1 to 12 eg:6")
    color_code= models.CharField(max_length=20)
    card_title= models.CharField(max_length=200)
    description = RichTextField()
    # card_footer=models.

class Dropdown(models.Model):	
	screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
	color_code= models.CharField(max_length=20, choices=COLOR_CHOICES)
	button_name=models.CharField(max_length=100)
	dropdown_item_name= models.CharField(max_length=100)

class Input(models.Model):
    INPUT_TYPES = [
        ('text', 'Text'),
        ('password', 'Password'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('datetime', 'Date and Time'),
        ('month', 'Month and Year'),
        ('week', 'Week'),
        ('search', 'Search'),
        ('tel', 'Telephone'),
        ('color', 'Color'),
        ('file', 'File Upload'),
        ('hidden', 'Hidden'),
        ('range', 'Range'),
        ('submit', 'Submit Button'),
        ('reset', 'Reset Button'),
        ('button', 'Generic Button'),
        ('image', 'Image Button'),
        ('datetime-local', 'Date and Time (Local)'),
        ('month', 'Month'),
    ]
    
    screen_name = models.ForeignKey(Screen, on_delete=models.CASCADE)
    field_size = models.IntegerField(default='12', help_text="Use a number from 1 to 12, e.g., 6")
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES)
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.BooleanField(blank=True, null=True)
    readonly = models.BooleanField(blank=True, null=True)
    required = models.BooleanField(blank=True, null=True)
    autofocus = models.BooleanField(blank=True, null=True)
    max = models.CharField(max_length=255, blank=True, null=True)
    min = models.CharField(max_length=255, blank=True, null=True)
    maxlength = models.PositiveIntegerField(blank=True, null=True)
    minlength = models.PositiveIntegerField(blank=True, null=True)
    step = models.CharField(max_length=255, blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)
    accept = models.CharField(max_length=255, blank=True, null=True)
    multiple = models.BooleanField(blank=True, null=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    list = models.CharField(max_length=255, blank=True, null=True)
    autocomplete = models.CharField(max_length=255, blank=True, null=True)
    spellcheck = models.BooleanField(blank=True, null=True)
    autocorrect = models.CharField(max_length=255, blank=True, null=True)
    autocapitalize = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.screen_name} - {self.input_type} Input"
	
class Modal(models.Model):
        MODAL_SIZE = [
        ('sm', 'Small'),
        ('lg', 'Large'),
        ('xl', 'Extra Large'),
        ]
        screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
        button_name= models.CharField(max_length=200)
        button_color= models.CharField(max_length=20, choices=COLOR_CHOICES)
        modal_size= models.CharField(max_length=20, choices=MODAL_SIZE)
        modal_color= models.CharField(max_length=200)
        modal_title= models.CharField(max_length=100)
        modal_description_type = models.CharField(max_length=100)
        modal_description=RichTextField(blank=True,null=True)
        formtable=models.ForeignKey(Table,on_delete=models.CASCADE,blank=True,null=True)
     

class FormWidget(models.Model):
    screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
    card_size=models.IntegerField(default='12',help_text="Use number from 1 to 12 eg:6")
    heading= models.CharField(max_length=250)
    formtable=models.ForeignKey(Table,on_delete=models.CASCADE)

    def __str__(self):
         return self.heading
    

class CardImages(models.Model):
     image=models.ImageField(upload_to='Card Image/')
     
class YourModel(models.Model):
    description = RichTextField()

class Menu(models.Model):
    menu_name=models.CharField(max_length=250,blank=True,null=True)
    position=models.IntegerField(blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE,blank=True,null=True)

class MainSubMenu(models.Model):
    main_submenu_name=models.CharField(max_length=250,blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
   
    def _str_(self):
         return self.main_submenu_name

class SubMenu(models.Model):
    menu = models.ForeignKey(MainSubMenu, on_delete=models.CASCADE,blank=True, null=True)
    sub_menu_name=models.CharField(max_length=250,blank=True,null=True)
    position=models.IntegerField(blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE,blank=True,null=True)

class IconMaster(models.Model):
    icon_name=models.CharField(max_length=200)
    icon_svg=models.TextField()

class Checkbox(models.Model):
    widget = models.ForeignKey(FormWidget, on_delete=models.CASCADE, null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)
    screen_version_name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)

class FieldSize(models.Model):
    screen_name = models.ForeignKey(Screen,on_delete=models.CASCADE,null=True, blank=True)
    formwidget = models.ForeignKey(FormWidget,on_delete=models.CASCADE,null=True, blank=True)
    tablename = models.ForeignKey(Table,on_delete=models.CASCADE,null=True, blank=True)
    fieldname = models.ForeignKey(Field,on_delete=models.CASCADE,null=True, blank=True)
    fieldsize = models.CharField(max_length=12,null=True, blank=True)

class UserTypeMaster(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    user_type=models.CharField(max_length=50)
    description=models.TextField()

class ScreenVersion(models.Model):
    verion_name=models.CharField(max_length=50)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserTypeMaster, on_delete=models.CASCADE)
    status=models.CharField(max_length=10, default="pending")

class ScreenVersionFields(models.Model):
    version = models.ForeignKey(ScreenVersion, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    column_size = models.IntegerField()
    label_name = models.CharField(max_length=50, blank=True,null=True)
    position = models.IntegerField(blank=True, null=True)

class Model_Identification(models.Model):
    model_id = models.CharField(max_length=50, blank=True,null=True)
    model_name = models.CharField(max_length=50, blank=True,null=True)
    model_type = models.CharField(max_length=50, blank=True,null=True)
    screen_name = models.CharField(max_length=50, blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)