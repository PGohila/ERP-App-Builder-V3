
import os
from typing import Tuple
import re
from .models import *
from django.http.response import HttpResponse
from .constant import SAMPLE_FILES,project_location,WIDGET_FILES

frontend_project_location = os.path.abspath("projects/Frontend/")
backend_project_location = os.path.abspath("projects/Backend/")


def to_camel_case(s):
    return ''.join(word.capitalize() for word in re.split('[^a-zA-Z0-9]', s) if word)

def process_to_underscore(input_string):
    # Replace spaces with underscores
    result = input_string.lower().replace(" ", "_")
    return result

def process_to_camel_case(input_string):
    # Split the string into words
    words = input_string.split()
    
    # Capitalize the first letter of each word and join them
    processed_string = ''.join([word.capitalize() for word in words])   
    return processed_string

def create_form(screen,tables):
    print('form start')
    for table in tables:
        table_name=table.name
        model_name=process_to_camel_case(table_name)
        new_project_directory = os.path.join(frontend_project_location,f'{screen.project.project_name}_frontend' )
        directory = os.path.join(new_project_directory,f"{screen.project.project_name}_frontend_app", 'forms.py')   
        template_form = f'''

class {model_name}Form(forms.Form):
'''   
        form_fields = Field.objects.filter(table=table)
        field_lines = []
        if form_fields.exists():
            field_lines = create_form_fields(form_fields=form_fields)
        with open(directory, 'a+') as form_file:
            form_file.write(template_form)
            form_file.writelines(field_lines)
    print('form end')


def create_form_fields(form_fields) -> "list[str]":
    field_lines = []
    for field in form_fields:
        field_name=process_to_underscore(field.field_name)
        ## this is for create form fields in created project
        if field.field_type == "CharField": 
            line = f'\t{field_name} = forms.CharField(max_length={field.max_length}' + \
                (', required=True' if field.required == "Required" else ', required=False') + \
                (f', help_text="{field.help_text}"' if field.help_text else '') + \
                ', widget=forms.TextInput(attrs={"class": "form-control"}))\n' 
        elif field.field_type == "IntegerField":
            line = f'\t{field_name} = forms.IntegerField(' + (f'validators=[MinValueValidator({field.min_length})],' if field.min_length is not None else '') + ('required=True,' if field.required == "Required" else 'required=False,') + 'widget=forms.NumberInput(attrs={"class": "form-control"}))\n'
        elif field.field_type == "BooleanField":
            line = f'\t{field_name} = forms.BooleanField(' + ('required=True,' if field.required == "Required" else 'required=False,') + 'widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))\n'
        elif field.field_type == "DateField":
            line = f'\t{field_name} = forms.DateField('+ (f'input_formats="{field.date_format}",' if field.date_format is not None else "input_formats=['%Y-%m-%d'],") +  ('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))\n'
        elif field.field_type == "DateTimeField":
            line = f'\t{field_name} = forms.DateTimeField(' + ('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.DateTimeInput(attrs={"type": "date","class": "form-control"}))\n'
        elif field.field_type == "FileField":   
            line = (
                f'\t{field_name} = forms.FileField(' +
                (f'validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]),') +
                (f'MaxValueValidator(limit_value={field.file_limit} * 1024 * 1024)],' if field.file_limit else '],') +
                ('required=True,' if field.required == "Required" else 'required=False,') +
                'widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))\n'
            )
        elif field.field_type == "FloatField":
            line = f'\t{field_name} = forms.FloatField(' + ('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.NumberInput(attrs={"class": "form-control"}))\n'
        elif field.field_type == "ForeignKey": 
            line = f'\t{field_name} = forms.CharField(' + (' required=True,' if field.required == "Required" else 'required=False,')  + ' widget=forms.Textarea(attrs={"class": "form-control"}))\n'
        elif field.field_type == "DecimalField":
            line = f'\t{field_name} = forms.DecimalField(max_digits={field.max_digits}, decimal_places={field.decimal_places},' + ('required=True,' if field.required == "Required" else ',required=False,') + ' widget=forms.NumberInput(attrs={"class": "form-control"}))\n' 
        elif field.field_type == "GenericIPAddressField":
            line = f'\t{field_name} = forms.GenericIPAddressField(protocol="both",unpack_ipv4=True,' + ('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.TextInput(attrs={"class": "form-control"}))\n' 
        elif field.field_type == "ImageField":
            line = f'\t{field_name} = forms.ImageField(' + ('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))\n'
        elif field.field_type == "ManyToManyField":
            line = f'\t{field_name} = forms.CharField(' + (' required=True,' if field.required == "Required" else 'required=False,')  + ' widget=forms.Textarea(attrs={"class": "form-control"}))\n'
        elif field.field_type == "OneToOneField":
            line = f'\t{field_name} = forms.CharField(' + (' required=True,' if field.required == "Required" else 'required=False,')  + ' widget=forms.Textarea(attrs={"class": "form-control"}))\n'
        elif field.field_type == "TextField":  
            line = f'\t{field_name} = forms.CharField(' + (' required=True,' if field.required == "Required" else 'required=False,')  + ' widget=forms.Textarea(attrs={"class": "form-control"}))\n'
        elif field.field_type == "TimeField":
            line = f'\t{field_name} =  forms.TimeField(input_formats=["%H:%M:%S"],'   +('required=True,' if field.required == "Required" else 'required=False,') + ' widget=forms.TimeInput(attrs={"class": "your-time-input-class form-control"}))\n'
        else:
            pass
        field_lines.append(line)
    return field_lines


######### create url ########

def create_curd_url(screen):
    print('curd url satrt')
    screen_name=process_to_underscore(screen.screen_name)
    project_name = f"{screen.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory,f"{project_name}_app", 'urls.py')
    template_url = [
        f'\tpath("{screen_name}/", {screen_name}, name="{screen_name}"),\n',
        f'\tpath("{screen_name}_edit/<pk>/", {screen_name}_edit, name="{screen_name}_edit"),\n',
        # f'\tpath("{screen_name}_view/<pk>/", {screen_name}_view, name="{screen_name}_view"),\n',
        f'\tpath("{screen_name}_delete/<pk>/", {screen_name}_delete, name="{screen_name}_delete"),\n',
        ']' 
    ]
    lines = []
    file = open(directory)
    for line in file:
        lines.append(line)

    with open(directory, 'w+') as url_file:
        lines = [line for line in lines if line != '\n']
        lines.pop()
        lines = lines + template_url
        url_file.writelines(lines)
    file.close()
    print('curd url end')


## this function for model creation to new project(backend)
def create_model(screen,tables):
    print('model start')
    for table in tables:
        table_name=table.name
        model_name=process_to_camel_case(table_name)
        new_project_directory = os.path.join(backend_project_location,f'{screen.project.project_name}_backend' )
        directory = os.path.join(new_project_directory,f"{screen.project.project_name}_backend_app", 'models.py')
        template_models = f'''

class {model_name}(models.Model):
'''
        model_fields = Field.objects.filter(table=table)

        field_lines = []
        if model_fields.exists():
            field_lines = create_model_fields(model_fields=model_fields)

        with open(directory, 'a+') as model_file:
            model_file.write(template_models)
            model_file.writelines(field_lines)
    print('model end')


## this function for model field creation to new project(backend)
def create_model_fields(model_fields) -> "list[str]":
    field_lines = []
    for field in model_fields:
        field_name=process_to_underscore(field.field_name)
        
        if field.field_type == "CharField": 
            line = f'\t{field_name} = models.CharField(max_length={field.max_length}' + (', blank=True, null=True' if field.required != "Required" else ', blank=False, null=False') + f', help_text="{field.help_text}")\n'
        elif field.field_type == "IntegerField":
            line = f'\t{field_name} = models.IntegerField(' + (f'validators=[MinValueValidator({field.min_length})],' if field.min_length is not None else '') + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "BooleanField":
            line = f'\t{field_name} = models.BooleanField(default={field.boolean_checkbox},' + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')
        elif field.field_type == "DateField":
            line = f'\t{field_name} = models.DateField(' + ('auto_now_add = True,' if field.auto_now_checkbox == True else ' auto_now_add = False,') + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')
        elif field.field_type == "DateTimeField":
            line = f'\t{field_name} = models.DateTimeField(' + ('auto_now_add = True,' if field.auto_now_checkbox == True else 'auto_now_add = False,') + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')
        elif field.field_type == "ForeignKey": 
            line = f'\t{field_name} = models.ForeignKey({process_to_camel_case(field.table_name.name)}, on_delete=models.CASCADE,' + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "FileField":   
            line = f'\t{field_name} = models.FileField(upload_to="documents/", ' + \
                (f'validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"]), ' +
                    f'MaxValueValidator(limit_value={field.file_limit * 1024 * 1024})], ' if field.file_limit else '') + \
                ('blank=True, null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')
        elif field.field_type == "FloatField":
            line = f'\t{field_name} = models.FloatField(' + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "DecimalField":
            line = f'\t{field_name} = models.DecimalField(max_digits={field.max_digits}, '+ (f'decimal_places={field.decimal_places},' if field.decimal_places else f'decimal_places=2,' ) + ('blank=True,null=True)\n' if field.required != "Required" else ',blank=False, null=False)\n') 
        elif field.field_type == "GenericIPAddressField":
            line = f'\t{field_name} = models.GenericIPAddressField(protocol="{field.ip_protocol}",unpack_ipv4=True,' + ('blank=True, null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "ImageField":
            line = f'\t{field_name} = models.ImageField(upload_to="images/",' + (f'height_field="{field.image_height}",' if field.image_height is not None else "" ) + (f'width_field="{field.image_width}",' if field.image_width is not None else "") +('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')  
        elif field.field_type == "ManyToManyField":
            line = f'\t{field_name} = models.ManyToManyField("{process_to_camel_case(field.many_to_many.name)}",' + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "OneToOneField":
            line = f'\t{field_name} = models.OneToOneField({process_to_camel_case(field.one_to_one.name)}, on_delete=models.CASCADE,' + ('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n') 
        elif field.field_type == "TextField":  
            line = f'\t{field_name} = models.TextField(' + (' blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')  
        elif field.field_type == "TimeField":
            line = f'\t{field_name} =  models.TimeField('  +('blank=True,null=True)\n' if field.required != "Required" else 'blank=False, null=False)\n')   
        else:
            line = f'\t{field_name} = models.{field.field_type}(' + ('blank=True,null=True, null=True)\n' if field.required != "Required" else ')\n')
        field_lines.append(line)
    return field_lines

def create_dunder_methods(field_name: str):
    dunder_str = f'''
    def __str__(self) -> str:
        return self.{field_name}
'''
def create_admin(screen,tables):
    print('admin start')
    project_name=f'{screen.project.project_name}_backend'
    new_project_directory = os.path.join(backend_project_location,project_name )
    directory = os.path.join(new_project_directory,f'{project_name}_app','admin.py')
    for tables in tables:
        table_name=tables.name
        model_name=process_to_camel_case(table_name)
        template_admin = f'''
admin.site.register ({model_name})
'''
        with open(directory, 'a+') as admin_file:
            admin_file.write(template_admin)
    print('admin end')


def create_header(screen):
    
    screen_name=process_to_underscore(screen.screen_name)
    project_name = f'{screen.project.project_name}_frontend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', f'{screen_name}.html')
    directory1=os.path.join(new_project_directory,'templates',f'{screen_name}_edit.html')
    header = '''
    {% extends 'base.html' %} \n {% block body_block %}
        '''
    with open(directory, 'a+') as screen_file:
        screen_file.write(header)
    with open(directory1, 'a+') as screen_file1:
        screen_file1.write(header)   
        
def create_footer(screen):
    screen_name=process_to_underscore(screen.screen_name)
    project_name = f'{screen.project.project_name}_frontend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory=os.path.join(new_project_directory,'templates',f'{screen_name}.html')
    directory1=os.path.join(new_project_directory,'templates',f'{screen_name}_edit.html')
    header = '''
\n {% endblock %}
'''
    with open(directory, 'a+') as screen_file:
        screen_file.write(header)
    with open(directory1, 'a+') as screen_file1:
        screen_file1.write(header)

def create_html_a_button(screen,forms_id):
    screen_name=process_to_underscore(screen.screen_name)
    new_project_directory = os.path.join(frontend_project_location, screen.project.project_name )
    directory=os.path.join(new_project_directory,'templates',f'{screen_name}.html')
    screen_a_buttons = A_Button.objects.filter(screen_name=screen)
    if screen_a_buttons.exists():
        for a_button in screen_a_buttons:
            with open(f'{WIDGET_FILES}/a_button.html', 'r') as a_button_file:
                edited_lines = []
                for line in a_button_file:
                    edited_line = line
                    if "<**url**>" in line:
                        edited_line = edited_line.replace(
                            "<**url**>", str(a_button.url_link))
                    elif "<**Color_code**>" in line:
                        edited_line = edited_line.replace(
                            "<**Color_code**>", a_button.color_code)
                    elif "<**Button_name**>" in line:
                        edited_line = edited_line.replace(
                            "<**Button_name**>", a_button.button_name.capitalize())

                    edited_lines.append(edited_line)
                edited_lines.append('\n')

                with open(directory, 'a+') as screen_file:
                    screen_file.writelines(edited_lines)

# this function for frontend html screen creation
def create_html_form(screen):
    screen_name=process_to_underscore(screen.screen_name)
    project_name=f'{screen.project.project_name}_frontend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory=os.path.join(new_project_directory,'templates',f'{screen_name}.html')
    directory1=os.path.join(new_project_directory,'templates',f'{screen_name}_edit.html')
    screen_forms = FormWidget.objects.filter(screen_name=screen)
    if screen_forms.exists():
        for form in screen_forms:
            with open(f'{WIDGET_FILES}/form.html', 'r') as form_file:
                edited_lines = []
                for line in form_file:
                    edited_line = line
                    if "<**Coloumn_size**>" in line:
                        edited_line = edited_line.replace("<**Coloumn_size**>", str(form.card_size))
                    if "<**Input_form_heading**>" in line:
                        edited_line = edited_line.replace("<**Input_form_heading**>", form.heading.capitalize())
                    edited_lines.append(edited_line)
                edited_lines.append('\n')
                with open(directory, 'a+') as screen_file:
                    screen_file.writelines(edited_lines)
                with open(directory1, 'a+') as screen_file1:
                    screen_file1.writelines(edited_lines)

def create_html_table(screen,tables):
    print('html table start')
    screen_name=process_to_underscore(screen.screen_name)
    project_name=f'{screen.project.project_name}_frontend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', f'{screen_name}.html')
    for table in tables:
        field_obj=Field.objects.filter(table=table)
        App_fields= [data.field_name for data in field_obj]
        with open(f'{WIDGET_FILES}/table.html', 'r') as f_view:
            in_main_html_lines = f_view.readlines()
            out_main_html_lines = []
            for line in in_main_html_lines:
                line = line.replace('\n', '')
                if '<**BB_App_Name**>' in line:
                    out_main_html_lines.append(line.replace('<**BB_App_Name**>', screen_name))
                elif '<**BB_fields_Headers**>' in line:
                    fields_code = []
                    for item in App_fields:
                        fields_code.append(f"<th>{str(item).replace('_', ' ')}</th>")
                    for fc_lines in fields_code:
                        out_main_html_lines.append("{}".format(fc_lines))
                elif '<**BB_fields_Datas**>' in line:
                    fields_code = []
                    for item in App_fields:
                        head = "{{data."
                        foot = "}}"
                        fields_code.append(f"<td>{head}{str(item).lower().replace(' ', '_')}{foot}</td>")
                    for fc_lines in fields_code:
                        out_main_html_lines.append("{}".format(fc_lines))
                elif '<**URL**>' in line:
                    out_main_html_lines.append(line.replace('<**URL**>', f"{str(screen_name.lower()).replace(' ', '_')}"))
                else:
                    out_main_html_lines.append(line)

        # write the final file
        out_rec = ''
        for lines in out_main_html_lines:
            out_rec += ("{}\n".format(lines))
        with open(directory, 'a+') as screen_file:
            screen_file.writelines(out_rec)
    print('html table end')

# this function for crud api views.py functions (frontend)
def create_curd_view(screen, tables):
    print('curd start')
    screen_name = process_to_underscore(screen.screen_name)
    project_name = f"{screen.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, f"{project_name}_app", 'views.py')

    for table in tables:
        table_name = table.name
        model_name = process_to_camel_case(table_name)

        join_url = os.path.join(SAMPLE_FILES,'sample_api_frontend_views.py')
        with open(join_url, 'r') as f_view:
            in_main_html_lines = f_view.readlines()
            out_main_html_lines = []

            for line in in_main_html_lines:
                line = line.replace('<**model_name**>', str(model_name).replace(' ', '_'))
                line = line.replace('<**screen_name**>', str(screen_name).replace(' ', '_'))
                line = line.replace('<**api_endpoint**>', str(screen_name).replace(' ', '_'))
                out_main_html_lines.append(line)

        # write the final file
        out_rec = ''.join(out_main_html_lines)

        with open(directory, "a") as file:
            file.write(out_rec)
    print('Curd end')



def create_view(screen):
    screen_name = process_to_underscore(screen.screen_name)
    new_project_directory = os.path.join(frontend_project_location,screen.project.project_name )
    directory = os.path.join(new_project_directory,f'{screen.project.project_name}_app', 'views.py')
    template_form = f'''
def {screen_name}(request):
\treturn render(request, "{screen_name}.html")
    '''
    with open(directory, 'a+') as form_file:
        form_file.write(template_form)

#  this is for frontend url.py
def create_url(screen):
    screen_name=process_to_underscore(screen.screen_name)
    project_name=f"{screen.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location,project_name )
    directory = os.path.join(new_project_directory,f'{project_name}_app', 'urls.py')
    template_url = [
        f'\tpath("{screen_name}/", {screen_name}, name="{screen_name}"),\n',
        ']' 
    ]
    lines = []
    file = open(directory)
    for line in file:
        lines.append(line)

    with open(directory, 'w+') as url_file:
        lines = [line for line in lines if line != '\n']
        lines.pop()
        lines = lines + template_url
        url_file.writelines(lines)
    file.close()

def create_html_card(screen):
    screen_name=process_to_underscore(screen.screen_name)
    project_name=f"{screen.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', f'{screen_name}.html')
    card_forms = Card.objects.filter(screen_name=screen)
    if card_forms.exists():
        for form in card_forms:
            with open(f'{WIDGET_FILES}/card.html', 'r') as form_file:
                edited_lines = []
                for line in form_file:
                    edited_line = line
                    if "<**Column_size**>" in line:
                        edited_line = edited_line.replace(
                            "<**Column_size**>", str(form.size_in_number))
                    elif "<**Color_code**>" in line:
                        edited_line = edited_line.replace(
                            "<**Color_code**>", form.color_code)
                    elif "<**Card_title**>" in line:
                        edited_line = edited_line.replace(
                            "<**Card_title**>", form.card_title)
                    elif "<**Card_description**>" in line:
                        edited_line = edited_line.replace(
                            "<**Card_description**>", form.description)

                    edited_lines.append(edited_line)
                edited_lines.append('\n')

                with open(directory, 'a+') as card_file:
                    card_file.writelines(edited_lines)


def modal_replace_placeholders(line, modal):
    print('modal replce palceholders start',modal)
    replacements = {
        "<**button_color**>": str(modal.button_color),
        "<**Button_name**>": modal.button_name,
        "<**modal_color**>": modal.modal_color,
        "<**Modal_Size**>": modal.modal_size,
        "<**Modal_title**>": modal.modal_title,
        "<**Button_id**>": process_to_underscore(modal.button_name)
    }
    if modal.modal_description_type == 'other':
       replacements["<**Modal_descriptions**>"]=modal.modal_description

    for placeholder, value in replacements.items():
        line = line.replace(placeholder, value)

    return line

def create_html_modal(screen):
    print('html modal start')
    screen_name = process_to_underscore(screen.screen_name)
    project_name=f'{screen.project.project_name}_backend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', f'{screen_name}.html')
    modals = Modal.objects.filter(screen_name=screen)

    if modals.exists():
        for modal in modals:
            try:
                if modal.modal_description_type == 'form':
                    html_page='modal_form.html'
                else:
                    html_page='modal.html'
                with open(f'{WIDGET_FILES}/{html_page}', 'r') as modal_file:
                    edited_lines = [modal_replace_placeholders(line, modal) for line in modal_file]
                    edited_lines.append('\n')

                    with open(directory, 'a+') as card_file:
                        card_file.writelines(edited_lines)
            except Exception as error:
                error('Error occurred: %s', error)
    print('html modal end')


def alert_replace_placeholders(line, modal):
    print('alert replce palceholders start',modal)
    replacements = {
        "<**Color_code**>": str(modal.color_code),
        "<**Alert_Description**>": modal.message
    }
    for placeholder, value in replacements.items():
        line = line.replace(placeholder, value)

    return line

def create_html_alert(screen):
    print("create_html_alert")
    screen_name = process_to_underscore(screen.screen_name)
    project_name=f'{screen.project.project_name}_frontend'
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', f'{screen_name}.html')
    alerts = Alert.objects.filter(screen_name=screen)
    if alerts.exists():
        for alert in alerts:
            try:
                with open(f'{WIDGET_FILES}/alerts.html', 'r') as alert_file:
                    print('alert_file')
                    edited_lines = [alert_replace_placeholders(line, alert) for line in alert_file]
                    edited_lines.append('\n')

                    with open(directory, 'a+') as card_file:
                        card_file.writelines(edited_lines)
            except Exception as error:
                error('Error occurred: %s', error)
    print('html alert end')

def create_main_menu(main_menu):
    print("create_main_menu",main_menu)
    screen_name = process_to_underscore(main_menu.screen_name.screen_name)
    project_name = f"{ main_menu.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location,project_name)

    directory = os.path.join(new_project_directory,'templates', 'base.html')

    with open(os.path.join(WIDGET_FILES, 'main_menu.html'), 'r') as form_file:
        edited_lines = []
        for line in form_file:
            edited_line = line
            if "<**screen_name**>" in line:
                edited_line = edited_line.replace("<**screen_name**>", screen_name)
            if "<**menu_name**>" in line:
                edited_line = edited_line.replace("<**menu_name**>", main_menu.menu_name)
            edited_lines.append(edited_line)
        edited_lines.append('\n')

    with open(directory, 'r') as f:
        lines = f.readlines()

    # Find the index of the line you want to replace
    index_to_replace = None
    for i, line in enumerate(lines):
        if '<!-- next menu -->' in line:
            index_to_replace = i
            break

    # If the line is found, replace it
    if index_to_replace is not None:
        # Replace the line with the edited content
        lines[index_to_replace:index_to_replace + 1] = edited_lines

        # Write the modified lines back to the file
        with open(directory, 'w') as f:
            f.writelines(lines)

    else:
        print("Line '<!-- next menu -->' not found in the file.")

def create_sub_menu(sub_menu):
    screen_name = process_to_underscore(sub_menu.screen_name.screen_name)
    project_name=f"{sub_menu.project.project_name}_frontend"
    new_project_directory = os.path.join(frontend_project_location, project_name)
    directory = os.path.join(new_project_directory, 'templates', 'base.html')

    with open(os.path.join(WIDGET_FILES, 'sub_menu.html'), 'r') as form_file:
        edited_lines = []
        for line in form_file:
            edited_line = line
            if "<**URL**>" in line:
                edited_line = edited_line.replace("<**URL**>", screen_name)
            if "<**sub_menu_name**>" in line:
                edited_line = edited_line.replace("<**sub_menu_name**>", sub_menu.sub_menu_name)
            
            if "<**main_menu**>" in line:
                edited_line = edited_line.replace("<**main_menu**>", sub_menu.menu.main_submenu_name)
            edited_lines.append(edited_line)
        edited_lines.append('\n')

    with open(directory, 'r') as f:
        lines = f.readlines()

    # Find the index of the line you want to replace
    sub_index_to_replace = None
    main_index_to_replace = None
    for i, line in enumerate(lines):
        if f'<!-- {sub_menu.menu.main_submenu_name}_sub_menu -->' in line:
            sub_index_to_replace = i
            break

    # If the line is found, replace it
    if sub_index_to_replace is not None:
        # Replace the line with the edited content
        lines[sub_index_to_replace:sub_index_to_replace + 1] = edited_lines

        # Write the modified lines back to the file
        with open(directory, 'w') as f:
            f.writelines(lines)
    else:
        for i, line in enumerate(lines):
            if '<!-- next menu -->' in line:
                main_index_to_replace = i
                break
    
    if main_index_to_replace is not None:
        # Replace the line with the edited content
        edited_lines = main_sub_menu(sub_menu,WIDGET_FILES)
        lines[main_index_to_replace:main_index_to_replace + 1] = edited_lines

        # Write the modified lines back to the file
        with open(directory, 'w') as f:
            f.writelines(lines)

    else:
        print("Line '<!-- next menu -->' not found in the file.")


def main_sub_menu(sub_menu,WIDGET_FILES):
    screen_name = process_to_underscore(sub_menu.screen_name.screen_name)
    with open(os.path.join(WIDGET_FILES, 'sub_main_menu.html'), 'r') as form_file:
        edited_lines = []
        for line in form_file:
            edited_line = line
            if "<**URL**>" in line:
                edited_line = edited_line.replace("<**URL**>", screen_name)
            if "<**sub_menu_name**>" in line:
                edited_line = edited_line.replace("<**sub_menu_name**>", sub_menu.sub_menu_name)
                
            if "<**main_menu**>" in line:
                edited_line = edited_line.replace("<**main_menu**>", sub_menu.menu.main_submenu_name)
            
            if "<**menu_number**>" in line:
                edited_line = edited_line.replace("<**menu_number**>", str(sub_menu.id))
            edited_lines.append(edited_line)
        edited_lines.append('\n')
    return edited_lines


def create_serializer(screen,tables):
    print('Serializer start')
    project_name = f"{screen.project.project_name}_backend"
    new_project_directory = os.path.join(backend_project_location, project_name)
    directory = os.path.join(new_project_directory,f"{project_name}_app", 'serializers.py')
    for table in tables:
        table_name=table.name
        model_name=process_to_camel_case(table_name)
        template_form = f'''
class {model_name}Serializer(serializers.ModelSerializer):
\tclass Meta:
\t\tmodel = {model_name}
\t\tfields = "__all__"\n
    '''
        with open(directory, 'a+') as form_file:
            form_file.write(template_form)
            
 
def create_api_curd_view(screen,tables):
    screen_name_caps=process_to_camel_case(screen.screen_name)
    project_name = f"{screen.project.project_name}_backend"
    new_project_directory = os.path.join(backend_project_location, project_name)
    directory = os.path.join(new_project_directory,f"{project_name}_app", 'views.py')
    for table in tables:
        table_name=table.name
        join_url = os.path.join(SAMPLE_FILES,'sample_api_view.py')
        Model_name=process_to_camel_case(table_name)
        with open(f'{join_url}', 'r') as f_view:
            in_main_html_lines = f_view.readlines()
            out_main_html_lines = []
            for line in in_main_html_lines:
                if '<**Model_Name**>' in line:
                    out_main_html_lines.append(line.replace('<**Model_Name**>', f"{str(Model_name).replace(' ', '_')}"))
                elif '<**Screen_Name**>' in line:
                    out_main_html_lines.append(line.replace('<**Screen_Name**>', f"{str(screen_name_caps).replace(' ', '_')}"))
                else:
                    out_main_html_lines.append(line)

        # write the final file
        out_rec = ''
        for lines in out_main_html_lines:
            lines = lines.replace('\n', '')
            out_rec += ("{}\n".format(lines))
        file = open(directory, "a")
        file.write(out_rec)
        file.close()
        print('Api Curd end')

def create_api_curd_url(screen):
    print('curd url satrt')
    screen_name_caps=process_to_camel_case(screen.screen_name)
    screen_name_small=process_to_underscore(screen.screen_name)
    project_name = f"{screen.project.project_name}_backend"
    new_project_directory = os.path.join(backend_project_location, project_name)
    directory = os.path.join(new_project_directory,f"{project_name}_app", 'urls.py')
    template_url = [
        f'\tpath("{screen_name_small}/", {screen_name_caps}ListCreateView.as_view(), name="{screen_name_small}-create"),\n',
        f'\tpath("{screen_name_small}/<pk>/", {screen_name_caps}RetrieveUpdateDestroyView.as_view(), name="{screen_name_small}-update"),\n',
        ']' 
    ]
    lines = [] 
    file = open(directory)
    for line in file:
        lines.append(line)

    with open(directory, 'w+') as url_file:
        lines = [line for line in lines if line != '\n']
        lines.pop()
        lines = lines + template_url
        url_file.writelines(lines)
    file.close()
    print('cued url end')
