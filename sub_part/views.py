from django.shortcuts import render, redirect, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseRedirect
from sub_part.models import *
from sub_part.forms import *
import subprocess
import os
import time
import shutil
from django.contrib import messages
# from .auto import views_py, models_py, forms_py
import time
import pandas as pd
from .create import *
from itertools import groupby
from .serializer import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,FileResponse
from PIL import Image
from django.core.management import execute_from_command_line
import zipfile
import importlib,json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import HttpResponse
from .resources import *
from tablib import Dataset
from tablib.formats._xlsx import XLSXFormat
from openpyxl import Workbook
from .constant import *
CURRENT_WORKDIR = os.getcwd()

PROJECTS_DIRECTORY = os.path.abspath("projects/")
EXCEL_BASE_PATH = 'D:\\BB Office\\GIT\\app_builder_csv\\ERPprojectfiles'

# Create your views here.
def get_projectid(request):
    request.session["project_ID"] = request.POST.get('my_value')
    response_data = { 'redirect_url': '/dashboard'  # Replace with your actual redirection URL
        }
    return JsonResponse(response_data, safe=True)

def dashboard(request):
    # Retrieve the logged-in project ID from the session
    project_id = request.session.get("project_ID")
    if project_id:
        # Get counts based on the logged-in project ID
        table_count = Table.objects.filter(project_id=project_id).count()
        screen_count = Screen.objects.filter(project_id=project_id).count()
        field_count = Field.objects.filter(table__project_id=project_id).count()
        context = {
            'screen_count': screen_count,
            'table_count': table_count,
            'field_count': field_count,
        }
        return render(request, "dashboard.html", context)
    else:
        # Handle the case when there is no logged-in project ID
        return render(request, "dashboard.html")

def project_list(request):
    template_name = 'project_list.html'
    project_list = os.listdir(PROJECTS_DIRECTORY)
    current_project = Project.objects.get(id =request.session["project_ID"])
    return render(request, template_name, {'project_list': current_project})

def is_valid_project_name(project_name):
    return bool(project_name) and '/' not in project_name and '\\' not in project_name

def download_project(request, project_name):

    if not is_valid_project_name(project_name):
        return HttpResponse("Invalid project name")
    
    downloads_path = os.path.expanduser('~/Downloads')
    zip_file_path = os.path.join(downloads_path, f'{project_name}_project.zip')
    
    # Check if frontend and backend folders exist
    frontend_path = os.path.join(PROJECTS_FRONTEND, f'{project_name}_frontend')
    backend_path = os.path.join(PROJECTS_BACKEND, f'{project_name}_backend')
    
    if not os.path.exists(frontend_path):
        return HttpResponse(f"{frontend_path} doesn't exist")
    
    if not os.path.exists(backend_path):
        return HttpResponse(f"{backend_path} doesn't exist")
    
    # Create a zip file and add contents from frontend and backend folders
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for folder_path in [frontend_path, backend_path]:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
    
    # Serve the zip file as a download
    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    
    return response



def create_project(request: HttpRequest):
    all_project = Project.objects.all().order_by('-id')
    form = ProjectCreationForm()
    if request.method == "POST":
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project_name: str = process_to_underscore(form.cleaned_data['project_name']) #projectname
            obj=form.save()
            obj.project_name=project_name
            obj.save()
            # calling creating_project function
            creating_project(f"{project_name}_frontend",'Frontend')
            creating_project(f"{project_name}_backend",'Backend')
            return redirect('success') 
    return render(request, 'landing_screen/landing_screen.html',{'all_project':all_project,"form":form,'create_project_active': 'active'})

#  In this function we excuting django comment for creating new django-project
def creating_project(project_name,project_folder):
    print('creating project start')
    subapp_name = f'{project_name}_app'  # Default sub-application name
    # Create a new directory for the main project
    new_project_directory = os.path.join(PROJECTS_DIRECTORY, project_folder, project_name)
    
    if os.path.exists(new_project_directory):
        return HttpResponse("project path exists")

    os.makedirs(new_project_directory,exist_ok=True)
    time.sleep(.5)
    try:
        # Create the main project using 'startproject' command
        project_created = subprocess.run(
            ['django-admin', 'startproject', project_name, new_project_directory])
    except Exception as e:
        print(e)
        return HttpResponse(e)

    # Paths for the new project and app
    new_project_directory = os.path.abspath(new_project_directory)
    # Create the sub-application inside the project directory
    app_created = subprocess.run(
        ['python', 'manage.py', 'startapp', subapp_name], cwd=new_project_directory)

    if app_created.returncode != 0:
        print(
            f"app had a problem when being created {app_created.stderr}")

    
    curr_app_path = os.path.abspath(f'{subapp_name}/')
    print("curr_app_path",curr_app_path)

    # if not os.path.exists(new_project_directory):
    #     return HttpResponse(f"{new_project_directory} doesn't exist")
    # if not os.path.exists(curr_app_path):
    #     return HttpResponse(f"{curr_app_path} doesn't exist")
    print("new_project_directory",new_project_directory)
    #to add the additional data into the project which has been created.
    add_additional_settings(new_project_directory)
    add_subapp_to_installed_apps(new_project_directory,subapp_name)
    add_static_media_settings(new_project_directory)
    add_template_dirs_setting(new_project_directory,project_name)
    add_url_include_statement(new_project_directory,subapp_name)
    add_import_statements(new_project_directory)
    add_debug_urlpattern(new_project_directory)
 
    time.sleep(.25)
    # move the entire project to the created project location
    move_files(os.path.join(new_project_directory, subapp_name), new_project_directory)
    SOURCE_STATIC_DESIGN_FILES = None
    if '_frontend' in project_name:
        SOURCE_STATIC_DESIGN_FILES = os.path.abspath("designs/frondend_files/")
    else:
        SOURCE_STATIC_DESIGN_FILES = os.path.abspath("designs/backend_files/")

    destination_code_path = os.path.join(
        new_project_directory, subapp_name)
    if not os.path.exists(SOURCE_STATIC_DESIGN_FILES):
        return HttpResponse(f"{SOURCE_STATIC_DESIGN_FILES} doesn't exist")

    if not os.path.exists(destination_code_path):
        return HttpResponse(f"{destination_code_path} doesn't exist")
    # Copy code and files to the specified location
    copy_code_files(SOURCE_STATIC_DESIGN_FILES, destination_code_path)

    # Move 'templates' and 'static' directories outside of 'sub_part'
    move_templates_static(new_project_directory, subapp_name)



def success(request: HttpRequest):
    return render(request, 'success.html')


# Start This Section is used to add additional configuration in the settings.py & urls.py in main app 
def add_subapp_to_installed_apps(project_name,subapp_name):
    settings_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'settings.py')

    with open(settings_path, 'r') as f:
        lines = f.readlines()

    # Find the line where INSTALLED_APPS is defined
    installed_apps_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('INSTALLED_APPS'):
            installed_apps_index = i
            break

    if installed_apps_index is not None:
        # Insert the subapp into INSTALLED_APPS
        lines.insert(installed_apps_index + 1, f"    '{subapp_name}',\n")
        lines.insert(installed_apps_index + 1, f"    'rest_framework',\n")

        with open(settings_path, 'w') as f:
            f.writelines(lines)
    else:
        print("Error: INSTALLED_APPS not found in settings.py")

def add_additional_settings(project_name):
    settings_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'settings.py')
    with open(settings_path, 'r') as f:
        lines = f.readlines()

    # Find the line where BASE_DIR is defined
    base_dir_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('BASE_DIR'):
            base_dir_index = i
            break

    if base_dir_index is not None:
        # Add additional configurations after BASE_DIR
        additional_settings = [
            "TEMPLATE_DIR = BASE_DIR/'templates'\n",
            "STATIC_DIR = BASE_DIR/'static'\n",
            "MEDIA_ROOT = BASE_DIR/'media'\n",
        ]

        lines = lines[:base_dir_index + 1] + additional_settings + lines[base_dir_index + 1:]

        with open(settings_path, 'w') as f:
            f.writelines(lines)
    else:
        print("Error: BASE_DIR not found in settings.py")


def add_static_media_settings(project_name):
    settings_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'settings.py')

    with open(settings_path, 'r') as f:
        lines = f.readlines()

    # Find the line where STATIC_URL is defined
    static_url_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('STATIC_URL'):
            static_url_index = i
            break

    if static_url_index is not None:
        # Define STATIC_DIR based on BASE_DIR
        static_dir = f"STATIC_DIR, \n"

        # Add additional configurations after STATIC_URL
        static_media_settings = [
            f"MEDIA_URL = '/media/'\n",
            f"STATICFILES_DIRS = [\n",
            f"    {static_dir}\n",
            "]",
        ]

        lines = lines[:static_url_index + 1] + static_media_settings + lines[static_url_index + 1:]

        with open(settings_path, 'w') as f:
            f.writelines(lines)
    else:
        print("Error: STATIC_URL not found in settings.py")

def add_template_dirs_setting(project_name,project_name1):
    
    settings_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'settings.py')

    project_name2 = None
    with open(settings_path, 'r') as f:
        lines = f.readlines()
    if "_backend" in project_name1:
        project_name2 = project_name1.replace("_backend", "")

    else:
        project_name2 = project_name1.replace("_frontend", "")
    project_id = Project.objects.filter(project_name = project_name2).last()
    print('project_id',project_id.id)
    # Find the line where "DIRS" is defined inside the TEMPLATES configuration
    templates_index = None
    templates_index1 = None
    last_line_number = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("'BACKEND': 'django.template.backends.django.DjangoTemplates',"):
            templates_index = i
        last_line_number = i
    if templates_index is not None:
        # Replace the empty list with [TEMPLATE_DIR] inside the "DIRS" list in TEMPLATES
        lines[templates_index + 1] = f'        "DIRS": [TEMPLATE_DIR],\n'
        
    else:
        print("Error: 'DIRS' not found in TEMPLATES configuration in settings.py")

    lines[last_line_number ] = f'\nPROJECT_ID = {project_id.id}\n'

    with open(settings_path, 'w') as f:
        f.writelines(lines)
    

def add_url_include_statement(project_name,subapp_name):
    urls_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'urls.py')

    with open(urls_path, 'r') as f:
        lines = f.readlines()

    # Find the line where urlpatterns is defined
    urlpatterns_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith('urlpatterns'):
            urlpatterns_index = i
            break

    if urlpatterns_index is not None:
        # Add the include statement inside urlpatterns
        include_statement = f"    path('', include('{subapp_name}.urls')),\n"
        lines.insert(urlpatterns_index + 1, include_statement)

        with open(urls_path, 'w') as f:
            f.writelines(lines)
    else:
        print("Error: 'urlpatterns' not found in urls.py")

def add_import_statements(project_name):
    urls_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'urls.py')

    with open(urls_path, 'r') as f:
        lines = f.readlines()

    # Check if necessary import statements are already present
    include_imported = any(line.strip() == "from django.urls import path, include" for line in lines)
    settings_imported = any(line.strip() == "from django.conf import settings" for line in lines)
    static_imported = any(line.strip() == "from django.conf.urls.static import static" for line in lines)

    # Find the index of the last import statement
    last_import_index = max(i for i, line in enumerate(lines) if line.strip().startswith("from django.urls import"))

    # Add missing import statements after the last import statement
    if not include_imported:
        lines.insert(last_import_index + 1, 'from django.urls import include\n')
    if not settings_imported:
        lines.insert(last_import_index + 1, 'from django.conf import settings\n')
    if not static_imported:
        lines.insert(last_import_index + 1, 'from django.conf.urls.static import static\n')

    with open(urls_path, 'w') as f:
        f.writelines(lines)

def add_debug_urlpattern(project_name):
    urls_path = os.path.join(project_name, project_name.split(os.path.sep)[-1], 'urls.py')

    with open(urls_path, 'r') as f:
        lines = f.readlines()

    # Find the line where urlpatterns is defined
    urlpatterns_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith(']'):
            urlpatterns_index = i
            break

    if urlpatterns_index is not None:
        # Add the include statement inside urlpatterns
        debug_urlpattern = 'if settings.DEBUG:\n    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n'
        lines.insert(urlpatterns_index + 1, debug_urlpattern)

        with open(urls_path, 'w') as f:
            f.writelines(lines)
    else:
        print("Error: 'urlpatterns' not found in urls.py")

# End...! This Section is used to add additional configuration in the settings.py & urls.py in main app 

# Call this function after creating the project

def move_files(source: str, destination: str):
    if os.path.exists(source):
        if os.path.exists(destination):
            print(f"Destination path '{destination}' already exists. Skipping move.")
        else:
            shutil.move(source, destination)
            print(f"Moved '{source}' to '{destination}'")
    else:
        print(f"Source path '{source}' does not exist. Unable to move files.")


def copy_code_files(source, destination):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)


def move_templates_static(project_directory, subapp_name):
    templates_source = os.path.join(
        project_directory, subapp_name, 'templates')
    static_source = os.path.join(project_directory, subapp_name, 'static')
    widget_source = os.path.join(project_directory, subapp_name, 'widgets')

    templates_destination = os.path.join(project_directory, 'templates')
    static_destination = os.path.join(project_directory, 'static')
    widget_destination = os.path.join(
        project_directory, 'templates', 'widgets')

    # Move 'templates' and 'static' directories to the main project directory
    if os.path.exists(templates_source):
        shutil.move(templates_source, templates_destination)

    if os.path.exists(static_source):
        shutil.move(static_source, static_destination)

    if os.path.exists(widget_source):
        shutil.move(widget_source, widget_destination)

def edit_screen(request, screen_id):
    screen = get_object_or_404(Screen, id=screen_id)
    fields = Field.objects.filter(screen=screen)
    if request.method == 'POST':
        screen_form = ScreenForm(request.POST, instance=screen)
        if screen_form.is_valid():
            screen_form.save()
        for field in fields:
            field_name = request.POST.get('field_name')
            field_type = request.POST.get('field_type')
            max_length = request.POST.get('max_length')
            required = request.POST.get('required')

            field.field_name = field_name
            field.field_type = field_type
            field.max_length = max_length
            field.required = required
            field.save()
        return redirect('success')
    else:
        screen_form = ScreenForm(instance=screen)
    return render(request, 'edit_screen.html', {'screen_form': screen_form, 'fields': fields})


def create_dbform(request: HttpRequest):
    projectid = request.session["project_ID"]
    get_project_detail = Project.objects.get(id = projectid)
    table_record=Table.objects.filter(project_id=projectid)
    field_record=Field.objects.filter(table__project_id=projectid)
    table_list=[data.name for data in table_record]
    if request.method == 'POST':
        screen_form = TableForm(request.POST)
        if screen_form.is_valid():
            project = screen_form.cleaned_data.get('project', None)
            field_names = request.POST.getlist('field_name')
            field_types = request.POST.getlist('field_type')
            required_fields = request.POST.getlist('required')
            table=Table(
                name=screen_form.cleaned_data.get('name', None),
                project_id = projectid,
            )
            table.save()
            current_table = Table.objects.last()
  
            for i in range(len(field_names)):
                print("maxlength",request.POST.get(f'max_length_{i}'))
                Field.objects.create(
                table_id= current_table.id,
                field_name=field_names[i],
                field_type=field_types[i],
                required=required_fields[i],
                max_length=request.POST.get(f'max_length_{i}',None),
                help_text=request.POST.get(f'help_text_{i}',None),
                date_format=request.POST.get(f'date_format_{i}',None),
                boolean_checkbox = ('True' if request.POST.get(f'checkbox_{i}') is not None else "False"),
                auto_now_checkbox= ('True' if request.POST.get(f'auto_now_checkbox_{i}') is not None else "False"), #datetime
                max_digits=request.POST.get(f'max_digits_{i}',None),
                file_limit=request.POST.get(f'file_limit_{i}',None),
                table_name_id=request.POST.get(f'table_name_{i}',None), #forignkey
                ip_protocol=request.POST.get(f'ip_protocol_{i}',None),
                image_height=request.POST.get(f'max_length_{i}',None),
                image_width=request.POST.get(f'image_width_{i}',None),
                min_length=request.POST.get(f'min_length_{i}',None),
                many_to_many_id=request.POST.get(f'many_to_many_{i}',None),
                one_to_one_id=request.POST.get(f'one_to_one_{i}',None),
                use_seconds_checkbox=('True' if request.POST.get(f'use_seconds_checkbox_{i}') is not None else "False"),
                )

            messages.success(
                request, 'Database Table and their related code generated successfully!')
            return redirect('create_dbform')

    else:
        screen_form = TableForm()
    return render(request, 'create_dbform.html', {'field_record':field_record,'get_project_detail':get_project_detail,'table_list':table_list,'screen_form': screen_form,'table_record':table_record, 'create_dbform_active': 'active'})

def removing_empty_str_from_list(list):
    filtered_messages = [message for message in list if message.strip()]
    return filtered_messages
def main_sub_menu_save(request):
    if request.method == 'POST':
        form1 = MainSubMenuForm(request.POST)
        if form1.is_valid():
            form1.project_id = request.session["project_ID"]
            form1.save()
            messages.success(request, 'Data saved successfully.')  # Redirect to a success page or another view
            return redirect('screen_elements')
        else:
            messages.success(request, form1.errors) 
            print('error',form1.errors)
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Process the image (resize, etc.) if needed
        image = Image.open(uploaded_file)
        # Perform any necessary image processing here

        # Save the image to your media directory or database
        image_model_instance = CardImages(image=uploaded_file)
        image_model_instance.save()

        # Return the image URL in the response media\Card Image
        return JsonResponse({'content': f'media/Card Image/{uploaded_file.name}', 'alt': 'Image Alt Text'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def screen_elements(request: HttpRequest):
    projectid = request.session["project_ID"]
    get_project_detail = Project.objects.get(id = projectid)
    main_sub_menu_record = MainSubMenu.objects.all()
    main_main_form = MainSubMenuForm()
    screens_record = Screen.objects.filter(project_id=projectid)
    text_form=YourModelForm()
    record_table = Table.objects.all()
    tables=[]
    if request.method == 'POST':
        screen_details_form = ScreenElementForm(request.POST)
        if screen_details_form.is_valid():
            screen_details_form.project=projectid
            screen = screen_details_form.save("Screen Successfully created")
            # menu
            new_menu_name=request.POST.get('new_menu_name')
            sub_main_menu=request.POST.get('sub_main_menu')
            if new_menu_name:
                main_menu=Menu.objects.create(
                    menu_name=new_menu_name,
                    project=screen_details_form.cleaned_data['project'],
                    screen_name=screen,
                )
                print("menu successfully created")
                create_main_menu(main_menu)   #created
            #  sub menu
            elif sub_main_menu:
                sub_menu=SubMenu.objects.create(
                    menu_id=sub_main_menu,
                    sub_menu_name=request.POST.get('sub_menu_name'),
                    project=screen_details_form.cleaned_data['project'],
                    screen_name=screen,
                )
                print("supposed is it submanu it also successfully created")
                create_sub_menu(sub_menu)
            
        else:
            print(screen_details_form.errors)
            messages.success(request, screen_details_form.errors)

        create_header(screen) # html header creating for screen

        alert_message = removing_empty_str_from_list(request.POST.getlist('alert_message'))
        alert_color_code = removing_empty_str_from_list(request.POST.getlist('alert_color_code'))
        # Alert creation in screen
        if len(alert_message) > 0:
            print("creating alert") # working
            try:
                for i in range(len(alert_message)):
                    alert = Alert.objects.create(
                        screen_name_id=screen.pk,
                        color_code=alert_color_code[i],
                        message=alert_message[i],
                    )
                else:
                    create_html_alert(screen)

            except Exception as e:
                print(e)            
        # a tag creation
        a_button_url_link = removing_empty_str_from_list(
            request.POST.getlist('a_button_url_link'))
        a_button_color_code = removing_empty_str_from_list(
            request.POST.getlist('a_button_color_code'))
        a_button_button_name = removing_empty_str_from_list(
            request.POST.getlist('a_button_button_name'))
        if len(a_button_url_link) > 0:
            print("createing a_button")
            a_button_id=[]
            try:
                for i in range(len(a_button_url_link)): # not working
                    link = A_Button.objects.create(
                        screen_name_id=screen.id,
                        url_link=a_button_url_link[i],
                        color_code=a_button_color_code[i],
                        button_name=a_button_button_name[i],
                    )
                    a_button_id.append(link.id)
                
                
            except Exception as e:
                print(e)
                
        # button Creation
        button_button_type = removing_empty_str_from_list(
            request.POST.getlist('button_button_type'))
        button_color_code = removing_empty_str_from_list(
            request.POST.getlist('button_color_code'))
        button_button_name = removing_empty_str_from_list(
            request.POST.getlist('button_button_name'))
        if len(button_button_name) > 0:
            print("createing button")
            try:
                for i in range(len(a_button_url_link)): # not working
                    button = Button.objects.create(
                        screen_name_id=screen.id,
                        button_type=button_button_type[i],
                        color_code=button_color_code[i],
                        button_name=button_button_name[i],
                    )              
            except Exception as e:
                print(e)

        dropdown_button_name = removing_empty_str_from_list(
            request.POST.getlist('dropdown_button_name'))
        dropdown_color_code = removing_empty_str_from_list(
            request.POST.getlist('dropdown_color_code'))
        dropdown_item_name = removing_empty_str_from_list(
            request.POST.getlist('dropdown_item_name'))
        
        if len(dropdown_button_name) > 0:
            print("creating dropdown button")
            try:
                for i in range(len(dropdown_button_name)):  # not working
                    dropdown = Dropdown.objects.create(
                        screen_name_id=screen.id,
                        color_code=dropdown_color_code[i],
                        button_name=dropdown_button_name[i],
                        dropdown_item_name=dropdown_item_name[i],
                    )
            except Exception as e:
                print(e)
                pass

        modal_color = removing_empty_str_from_list(request.POST.getlist('modal_color'))
        modal_button_color = removing_empty_str_from_list(request.POST.getlist('modal_button_color'))
        modal_button_name = removing_empty_str_from_list(request.POST.getlist('modal_button_name'))
        modal_size = removing_empty_str_from_list(request.POST.getlist('modal_size'))
        modal_modal_title = removing_empty_str_from_list(request.POST.getlist('modal_modal_title'))
        modal_description_editor = removing_empty_str_from_list(request.POST.getlist('modal_description_editor'))
        modal_description_type = removing_empty_str_from_list( request.POST.getlist('modal_modal_description_type'))
        modal_description_table = removing_empty_str_from_list(request.POST.getlist('modal_description_table'))

        if len(modal_modal_title) > 0:
            print("creating model, table in screen")
            try:
                for i in range(len(modal_modal_title)): 
                    modal = Modal.objects.create(
                        screen_name_id=screen.id,
                        modal_color=modal_color[i],
                        button_color=modal_button_color[i],
                        button_name=modal_button_name[i],
                        modal_size=modal_size[i],
                        modal_title=modal_modal_title[i],
                        modal_description_type=modal_description_type[i],
                    )
                    print("successfully created modal")
                    if modal.modal_description_type == "form":
                        table_obj=Table.objects.get(id=modal_description_table[i])
                        modal.formtable=table_obj
                        modal.save()
                        tables.append(modal.formtable)
                    elif modal.modal_description_type == "other":
                        modal.modal_description=modal_description_editor[i]
                        modal.save()             
                else:
                    create_html_modal(screen)
                    create_html_table(screen,tables)
            except Exception as e:
                print(e)

        form_card_size = removing_empty_str_from_list(request.POST.getlist('form_card_size'))
        form_heading = removing_empty_str_from_list(request.POST.getlist('form_heading'))
        form_formtable = removing_empty_str_from_list(request.POST.getlist('form_formtable'))
        formtable_fields_value = removing_empty_str_from_list(request.POST.getlist('field_size1'))

        if len(form_formtable) > 0:
            print("create html formwidgets")
            try:
                for i in range(len(form_formtable)):    
                    form_widget = FormWidget.objects.create(
                        screen_name_id=screen.id,
                        card_size=form_card_size[i],
                        heading=form_heading[i],
                        formtable_id=form_formtable[i],
                    )
                    tables.append(form_widget.formtable)
                else:
                    create_html_form(screen)
                    create_html_table(screen,tables)
                    
            except Exception as e:
                print(e)

        card_size_in_number = removing_empty_str_from_list(
            request.POST.getlist('card_size_in_number'))
        card_color_code = removing_empty_str_from_list(
            request.POST.getlist('card_color_code'))
        card_card_title = removing_empty_str_from_list(
            request.POST.getlist('card_card_title'))
        card_card_description = removing_empty_str_from_list(
            request.POST.getlist('description'))
        if len(card_size_in_number) > 0:
            print("create card in screen")
            try:
                for i in range(len(card_size_in_number)):
                    card = Card.objects.create(
                        screen_name_id=screen.id,
                        size_in_number=card_size_in_number[i],
                        color_code=card_color_code[i],
                        card_title=card_card_title[i],
                        description=card_card_description[i],
                    )
                else:
                    create_html_card(screen)
            except Exception as e:
                print('error in card',e)

        
        if len(tables) > 0:
            #  suppose form used the model table then this condition statisfied
           
            app_name  = f'{screen.project.project_name}'
            create_curd_view(screen,tables)
            create_form(screen,tables)
            create_serializer(screen,tables)
            create_model(screen,tables)
            create_api_curd_view(screen,tables)
            backend_makemigration(app_name)
            create_curd_url(screen)
            create_api_curd_url(screen)
            create_admin(screen,tables)
            
        else:
            # create_view(screen)
            create_url(screen)
        create_footer(screen)
        messages.success(request, 'Data Saved successfully!')
        return redirect("screen_elements")  # Redirect to the overview screen

    else:
        screen_details_form = ScreenElementForm()
        modal_form = ModalForm()
        table_query=Table.objects.all()
    context = {
        'screen_details': screen_details_form,'main_main_form':main_main_form,
        'screen_elements_active': 'active','table_query':table_query,
        'record_table': record_table,'modal_form':modal_form,
        'screens_record':screens_record,'text_form':text_form,'main_sub_menu_record':main_sub_menu_record,'get_project_detail':get_project_detail
    }
    return render(request, 'screen_element_1.html', context)


def frontend_makemigration(app_name):
    project_location = os.path.abspath("projects/Frontend")
    app_name=f'{app_name}_frontend'
    execute_makemigrations(app_name,project_location)

def backend_makemigration(app_name):
    project_location1 = os.path.abspath("projects/Backend")
    app_name=f'{app_name}_backend'
    execute_makemigrations(app_name,project_location1)

def execute_makemigrations(app_name,project_location1):
    try:
        # Set the environment variable to point to the settings module
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{app_name}.settings'
        
        # Change to the target project directory
       
        new_project_directory = os.path.join(project_location1,app_name)
        print("new_project_directory",new_project_directory)
        os.chdir(new_project_directory)
        
        # Run makemigrations
        result = subprocess.run(['python', 'manage.py', 'makemigrations'], check=True, capture_output=True)
        # Run migrate
        migrate_result = subprocess.run(['python', 'manage.py', 'migrate'], check=True, capture_output=True)
        print(migrate_result.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print(f"Error during 'makemigrations' or 'migrate': {e}")
        print(e.stderr.decode('utf-8'))
    finally:
        # Reset the environment variable to its original state
        os.environ['DJANGO_SETTINGS_MODULE'] = ''

def screen_element_with_orchestration(request):
    context={
        'screen_element_with_orchestration_active':'active'
    }
    return render(request, 'screen_element_with_orchestration.html', context)


# def upload_excel(request):
#     try:
#         projectid = request.session["project_ID"]
#         get_project_detail = Project.objects.get(id = projectid)
#         print("projectid",projectid)
#         if request.method == 'POST':
#             form = ExcelUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 excel_file = request.FILES['excel_file']
#                 dataset = Dataset()
#                 # getting excel file and read
#                 new_data = request.FILES['excel_file'].read() 
#                 dataset.load(new_data, format='xlsx', sheet_name='tabledata')
#                 table_source = TableResource()
#                 result = table_source.import_data(dataset,dry_run=True)
#                 if  not result.has_errors():
#                     aa=table_source.import_data(dataset,dry_run=False)
#                     print("error",aa)

#                 # try:
#                 #     # Read the Excel file with multiple sheets
#                 #     xls = pd.ExcelFile(excel_file)

#                 #     # Iterate over each sheet and create instances for each model
#                 #     for sheet_name in xls.sheet_names:
#                 #         df = xls.parse(sheet_name)

#                 #         # Determine the form class based on the sheet name
#                 #         FormClass = get_form_class(request,sheet_name,df)

#                 #         # Iterate over each row and create instances

#                 #     return redirect('success')  # Redirect to a success page

#                 # except Exception as e:
#                 #     return render(request, 'upload_excel.html', {'form': form, 'error_message': str(e)})
#         else:
#             form = ExcelUploadForm()
#         return render(request, 'upload_excel.html', {'form': form, 'upload_excel_active': 'active'})
#     except Exception as e:
#         return render(request, 'upload_excel.html', {'form': form, 'error_message': str(e)})




def get_form_class(request,sheet_name,df):
    # Determine the form class based on the sheet name
    if sheet_name == 'Project Sheet':
        print(1)
        FormClass=ProjectCreationForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Screen Sheet':
        print(2)
        FormClass=ScreenForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Table Sheet':
        print(3)
        FormClass=TableForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Field Sheet':
        print(4)
        FormClass=FieldForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Form Sheet':
        print(5)
        FormClass=FormForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'View Sheet':
        print(6)
        FormClass=ViewForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Widget Sheet':
        print(7)
        FormClass=FormWidgetForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'A_Button Widget':
        print(8)
        FormClass=A_ButtonForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Alert Widget':
        print(9)
        FormClass=AlertForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Button Widget':
        print(10)
        FormClass=ButtonForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Card Widget':
        print(11)
        FormClass=CardForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Dropdown Widget':
        print(12)
        FormClass=DropdownForm
        process_excel_rows(request, FormClass, df)
    if sheet_name == 'Form Widget':
        print(13)
        FormClass=FormForm
        process_excel_rows(request, FormClass, df)
    return True
    # Add other forms as needed

def process_excel_rows(request, FormClass, df):
    # Iterate over each row and create instancesx
    for _, row in df.iterrows():
        try:
            form_instance = FormClass(data=row)
            if form_instance.is_valid():
                instance = form_instance.save()
            else:
                print(form_instance.errors)

        except Exception as e:
            print(f"An error occurred: {e}")

def icon_master(request):
    form=IconMasterForm()
    records=IconMaster.objects.all()
    if request.method=='POST':
        form=IconMasterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Saved successfully!')
            return redirect('icon_master')
        else:
            messages.warning(request, form.errors)
    context={
        'records':records,'form':form
    }
    return render(request, 'icon_master.html',context)

def select_screen(request):
    project_name11 = Project.objects.get(id=request.session["project_ID"])
    screen_records = Screen.objects.filter(project_id = request.session["project_ID"])
    form = YourForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        selected_screen_id = form.cleaned_data.get('selected_screen_id')
        # Handle the selected_screen_id, for example, redirect to the preview screen
        if selected_screen_id:
            return redirect('preview_screen', screen_id=selected_screen_id)
    context = {
        'screen_records': screen_records,
        'select_screen_active': 'active',
        'form': form,
    }
    return render(request, 'select_screen.html', context)

def screen_version_list(request, screen_id):
    screen_version_records = ScreenVersion.objects.filter(screen_id = screen_id)
    context = {
        'screen_version_records': screen_version_records,
        'screen_version': 'active','screen_id':screen_id
    }
    return render(request, 'screen_version_list.html', context)

def screen_version_s1(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    form=FormWidget.objects.filter(screen_name=screen).last()
    form_table=form.formtable
    # tabl
    user_type_records = UserTypeMaster.objects.filter(project= request.session["project_ID"])
    if request.method == 'POST':
        screen_version_name=request.POST.get('screen_version_name')
        user_type=request.POST.get('user_type')
        screen_version=ScreenVersion.objects.create(
            verion_name=screen_version_name,
            screen=screen,
            project_id=request.session["project_ID"],
            user_type_id=user_type
        )
        return HttpResponseRedirect(f"/screen_version_s2/{screen_version.id}/")
    context = {
        'screen': screen,'user_type':user_type_records,
    }
    return render(request, 'screen_version_s1.html', context)

def screen_version_s2(request, screen_version_id):
    screen_version = get_object_or_404(ScreenVersion, pk=screen_version_id)
    screen_version_fields = ScreenVersionFields.objects.filter(version=screen_version_id)
    form_widgets = FormWidget.objects.filter(screen_name=screen_version.screen).last()
    form_table=form_widgets.formtable
    fields=Field.objects.filter(table=form_table)
    exisiting_fields=[]
    new_fields=[]
    screen_version_fields_list=[data.field for data in screen_version_fields]
    for field in fields:
        new_fields.append(field)
        if field in screen_version_fields_list:
            exisiting_field = screen_version_fields.filter(field=field).last()
            exisiting_fields.append(exisiting_field)
        else:
            exisiting_fields.append(None)
    NewFields_and_ExisitingFields=zip(new_fields,exisiting_fields)

    if request.method == 'POST':
        field_id_list=request.POST.getlist('field')
        for field_id in field_id_list:
            print('field_id,column_size',field_id)
            column_size_key = f'column_size_{field_id}'
            column_size_value = request.POST.get(column_size_key, None)
            print('column_size_value',column_size_value)
            screen_field = screen_version_fields.filter(field_id=field_id)
            if column_size_value is not None and not screen_field.exists():
                obj=ScreenVersionFields(
                    version=screen_version,
                    field_id=field_id,
                    column_size=column_size_value
                )
                obj.save()
        return HttpResponseRedirect(f"/screen_version_s3/{screen_version_id}")
    context = {
        'fields':fields,'screen_version_fields':screen_version_fields,'NewFields_and_ExisitingFields':NewFields_and_ExisitingFields
    }
    return render(request, 'screen_version_s2.html', context)

def screen_version_s3(request, screen_version_id):
    # getting selected version fields
    screen_version_fields = ScreenVersionFields.objects.filter(version=screen_version_id).order_by('position')
    #  getting screen name
    screen_name=screen_version_fields[0].version.screen.screen_name
    if request.method == 'POST':
        label_list=request.POST.getlist('label')
        field_id_list=request.POST.getlist('field_id')
        count = 1
        #  looping label_list and field_id_list
        #  and get each data from ScreenVersionFields table and upading position and label name
        for label,field_id in zip(label_list,field_id_list):
            screen_version_field=ScreenVersionFields.objects.get(id = field_id)
            screen_version_field.position=count
            screen_version_field.label_name=label
            screen_version_field.save()
            count += 1
        return HttpResponseRedirect(f"/screen_preview/{screen_version_id}")
    context = {
        'screen_version_field':screen_version_fields,'screen_name':screen_name,'screen_version_id':screen_version_id
    }
    return render(request, 'screen_version_s3.html', context)

def screen_preview(request, screen_version_id):
    # getting selected version fields
    screen_version = get_object_or_404(ScreenVersion, pk=screen_version_id)
    secreen_fields= ScreenVersionFields.objects.filter(version_id=screen_version).order_by('position')
    if request.method == 'POST':
        
        return HttpResponseRedirect(f"/select_screen/")
    context = {
        'screen_version':screen_version,'secreen_fields':secreen_fields
    }
    return render(request, 'screen_preview.html', context)

def preview_screen(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    user_type = UserTypeMaster.objects.filter(project= request.session["project_ID"])
    alerts = Alert.objects.filter(screen_name=screen)
    a_buttons = A_Button.objects.filter(screen_name=screen)
    buttons = Button.objects.filter(screen_name=screen)
    dropdowns = Dropdown.objects.filter(screen_name=screen)
    modals = Modal.objects.filter(screen_name=screen)
    cards = Card.objects.filter(screen_name=screen)
    form_widgets = FormWidget.objects.filter(screen_name=screen)
    form_widget_tables = [form_widget.formtable for form_widget in form_widgets if form_widget.formtable]
    
    if request.method == 'POST':
        screen_version_name = request.POST.get('screen_version_name')

        for modal in modals:
            checkbox_name = f'checkbox_for_modal_{modal.id}'
            is_checked = request.POST.get(checkbox_name) == 'on'
            Checkbox.objects.create(widget=modal, screen_version_name=screen_version_name, is_checked=is_checked)

        for form_widget in form_widgets:
            checkbox_name = f'checkbox_for_form_widget_{form_widget.id}'
            is_checked = request.POST.get(checkbox_name) == 'on'
            Checkbox.objects.create(widget=form_widget, screen_version_name=screen_version_name, is_checked=is_checked)


    context = {
        'screen': screen,
        'alerts': alerts,
        'a_buttons': a_buttons,
        'buttons': buttons,
        'dropdowns': dropdowns,
        'modals': modals,
        'cards': cards,
        'form_widgets': form_widgets,
        'form_widget_tables': form_widget_tables,'user_type':user_type,
    }

    return render(request, 'preview_screen.html', context)

def tables(request: HttpRequest):
    project_id = request.session.get("project_ID")

    record_table = Table.objects.filter(project_id=project_id)
    context={
        'record_table': record_table,
        'Priority_table':'active',
    }
    return render(request, 'dummy/tables.html',context)
def ajax_get_table_id(request):
    get_table_id = request.GET.get("table_id")
    table_fields = Field.objects.filter(table_id = get_table_id)
    data = list(table_fields.values("id","field_name"))
    print(data)
    return JsonResponse(data,safe=False)

def user_type_master(request):
    form=UserTypeMasterForm()
    records=UserTypeMaster.objects.filter(project_id=request.session["project_ID"])
    if request.method=='POST':
        form=UserTypeMasterForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.project_id=request.session["project_ID"]
            obj.save()
            messages.success(request, 'Data Saved successfully!')
            return redirect('user_type_master')
        else:
            messages.warning(request, form.errors)
    context={
        'records':records,'form':form
    }
    return render(request, 'user_type_master.html',context)

# this  function for the giving screen version details to new project 
class SetupView(APIView):
    def get(self,request, *args, **kwargs):
        records = UserTypeMaster.objects.all()
        screens = Screen.objects.all()
        screenversion = ScreenVersion.objects.all()
        screenversionfields = ScreenVersionFields.objects.all()
        serializer1 = UserTypeMasterSerializer(records, many=True) 
        serializer2 = ScreenSerializer(screens, many=True)
        serializer3 = ScreenVersionSerializer(screenversion, many=True) 
        serializer4 = ScreenVersionFieldsSerializer(screenversionfields, many=True)
        tables_list = [serializer1,serializer2,serializer3,serializer4]
        data_list = []
        for serializer in tables_list:
            data_list.append(serializer.data)
        return Response(data_list)
    
    def post(self, request):
        serializer1 = ProjectIDSerializer(data = request.data)
        if serializer1.is_valid():
            records = UserTypeMaster.objects.filter(project_id = request.data["project_id"])
            screens = Screen.objects.filter(project_id = request.data["project_id"])
            screenversion = ScreenVersion.objects.filter(project_id = request.data["project_id"])
            serializer1 = UserTypeMasterSerializer(records, many=True) 
            serializer2 = ScreenSerializer(screens, many=True)
            serializer3 = ScreenVersionSerializer(screenversion, many=True) 
            tables_list = [serializer1,serializer2,serializer3]
            data_list = []
            for serializer in tables_list:
                data_list.append(serializer.data)
        return Response(data_list, status=status.HTTP_201_CREATED)
    
# this function for export the all table records
def demo_excel_export(request):
    workbook = Workbook()
    model_resource = TableResource()
    model_resource1 = FieldResource()
    screen_resource = ScreenResource()
    argument_resource = ArgumentResource()
    form_resource = FormResource()
    widget_resource = WidgetResource()
    alert_resource = AlertResource()
    usertype = UserTypeMasterResource()
    fieldsize_resource = FieldSizeResource()
    checkbox_resource = CheckboxResource()
    iconmaster_resource = IconMasterResource()
    submenu_resource = SubMenuResource()
    mainsubmenu_resource = MainSubMenuResource()
    menu_resource = MenuResource()
    cardimage_resource = CardImagesResource()
    formwidget_resource = FormWidgetResource()
    modal_resource = ModalResource()
    input_source = InputResource()
    dropdown_resource = DropdownResource()
    card_resource = CardResource()
    button_resource = ButtonResource()
    a_button = A_ButtonResource()

    def add_headers(sheet,header):
        sheet.append(header)

    # export the table data
    dataset = model_resource.export()
    sheet1 = workbook.active  # using the first active sheet in workbook
    sheet1.title = "tabledata"
    add_headers(sheet1,model_resource.get_export_headers())
    for row in dataset:
        sheet1.append(row)

    def export_to_sheet(resource, title):
        dataset = resource.export()
        sheet = workbook.create_sheet(title=title)
        add_headers(sheet, resource.get_export_headers())
        for row in dataset:
            sheet.append(row)

    export_to_sheet(model_resource1, "fielddata")
    export_to_sheet(screen_resource, "screen_table")
    export_to_sheet(argument_resource, "argument_table")
    export_to_sheet(form_resource, "formtable")
    export_to_sheet(widget_resource, "widget_table")
    export_to_sheet(alert_resource, "alert_table")
    export_to_sheet(usertype, "usertypemaster")
    export_to_sheet(fieldsize_resource, "fieldsize_table")
    export_to_sheet(checkbox_resource, "checkbox_table")
    export_to_sheet(iconmaster_resource, "iconmaster")
    export_to_sheet(submenu_resource, "submenu")
    export_to_sheet(mainsubmenu_resource, "mainsubmenu")
    export_to_sheet(menu_resource, "menu_table")
    export_to_sheet(cardimage_resource, "cardimage")
    export_to_sheet(formwidget_resource, "formwidget")
    export_to_sheet(modal_resource, "modal_creation")
    export_to_sheet(input_source, "input_creation")
    export_to_sheet(dropdown_resource, "dropdown_creation")
    export_to_sheet(card_resource, "card_creation")
    export_to_sheet(button_resource, "button_creation")
    export_to_sheet(a_button, "a_button_creation")
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="your_model_data.xlsx"'
    workbook.save(response)
    return response

def upload_excel(request):
    # try:
        projectid = request.session["project_ID"]
        print("projectid",projectid)
        tables1=[]
        if request.method == 'POST':
            excel_file = EXCEL_BASE_PATH
            excel_file1 = 'Screenslist.csv' #screenlist csv path

            file = os.path.join(excel_file,excel_file1)
            response = excel_to_screen(excel_file,projectid)
            if response:
                print('sucess')
                return redirect('upload_excel')
            else:
                print('fail')
                return redirect('upload_excel')
        return render(request, 'upload_excel.html', { 'upload_excel_active': 'active'})

from .script import *

def model_identifications(screen, modeltype,projectid):
    # try:
        model_identify = Model_Identification.objects.filter(project_id = projectid)
        if model_identify.filter(screen_name = screen).exists():
            response ={
                'status_code':1,
                'error_message':'Already screen is exists'
            }
            return response
        model_identify_count = model_identify.count()
        uniqueid = model_id_generation('MI' , (model_identify_count + 1))
        # generate model name for particular project
        model_name = model_name_generation('User_',model_identify_count + 1,projectid)
   
        model_identify = model_identify.create(
            model_id=uniqueid,
            model_name=model_name,
            model_type=modeltype,
            screen_name = screen,
            project_id = projectid,
        )
        response ={
            'status_code':0,
            'screen_name':model_identify.model_name
        }
        return response


def excel_to_screen(base_path,project_id):
    projectid = project_id # project id
    BASE_DIR = base_path # excel base directory
    screen_list_csv = 'Screenslist.csv' # screen list excel 
    screen_details_dir = 'ScreenDetailCSVs' # screnn detail excles directory
    create_folder = create_folder_and_csv(projectid)
    df = pd.read_csv(os.path.join(BASE_DIR,screen_list_csv)) # reading screen list excel
    grouped_data = df.groupby('sub_module')['screen_name'] # grouping screen name based on sub_module
    for sub_module,screen_list in grouped_data:  #looping groups
        count = 0
        screen_list=list(screen_list) # spliting screen list in group
        for screen in screen_list: # looping screens from screen list
            screen_file_name  = space_to_underscore(screen) # removing space and adding underscore
            unwanted_screen_list = ['Unfortunately','csv',''] # list of unwanted screen name
            # if unwanted screen is exits skiping that loop
            if screen_file_name in unwanted_screen_list:
                continue
            # joining the excel base directory and screnn detail excles directory and screen name with .csv
            screen_details_csv = os.path.join(BASE_DIR,screen_details_dir,str(screen_file_name)+'.csv')
            # in that path file is existing or not, if exists it will go to next step
            if os.path.isfile(screen_details_csv):
                
                print('file exists',screen_details_csv)
                # reading screen detail from csv
                table_df = pd.read_csv(screen_details_csv)
                # saving screen name into model indentifier table and returing alternative screen name using this screen name we are going to create models,forms,views...etc
                screen_response = model_identifications(screen,"User_model",projectid)
                if screen_response['status_code'] == 1:
                    continue
                count+=1
                screen_name = screen_response['screen_name']
                # saving data into screen and menu tables
                screen_obj = Screen.objects.create(screen_name=screen_name, project_id=projectid)
                main_menu_obj = MainSubMenu.objects.filter(main_submenu_name=sub_module).last()
                if not main_menu_obj:
                    main_menu_obj = MainSubMenu.objects.create(main_submenu_name=sub_module,project_id = projectid )
                response = listing_created_screen(create_folder,screen,main_menu_obj.main_submenu_name)
                sub_menu_obj = SubMenu.objects.create(menu=main_menu_obj,sub_menu_name=screen,project_id=projectid,screen_name=screen_obj)
                create_sub_menu(sub_menu_obj)
                create_header(screen_obj)
                # creating tables and field
                table_obj = Table.objects.create(name=screen_name,project_id=projectid)
                table_file = create_tables_files(response,projectid)
                for index, row in table_df.iterrows(): # Process each row
                    # from row getting field name and field type
                    get_field_name = row.iloc[0]
                    field_type=row.iloc[1]
                    field_name = remove_special_characters(get_field_name) # removing spl charater 
                    field_validaion = field_name_validate(field_name,table_obj.id) # validating field name 
                    field_type_valid = validate_field_type(field_type) # validating field type
                    if  field_validaion and field_type_valid: # field name and field type is valid then will process into next step
                        table_dic={} # creating empty dictonary
                        add_fields_csv(table_file,remove_special_characters(field_name))
                        # aading name and value into dictonary
                        table_dic['table']=table_obj
                        table_dic['field_name']=remove_special_characters(field_name)
                        table_dic['field_type']=field_type
                        if field_type == 'CharField':
                            try:
                                field_length = row.iloc[2]
                                field_length = eval(field_length)
                                if isinstance(field_length,int) :
                                    table_dic['max_length']=field_length
                                else:
                                    table_dic['max_length']=250
                            except:
                                table_dic['max_length']=250
                 
                        mandatory = row.iloc[4]
                        if mandatory == 'yes':
                            table_dic['required']='Required'
                        else:
                            table_dic['required']='non-Required'
                        # saving into field table 
                        Field.objects.create(**table_dic)

                    # elif and else are error catching
                    elif field_validaion is False:
                        error_message=f"\n{field_name}- field name is not valid (screen name - {screen})  {field_validaion}  {field_type_valid}"
                        error_log(error_message)
                    else:
                        error_message=f"\n{field_type}- field type is not valid (screen name - {screen}, field name - {field_name}) {field_validaion}  {field_type_valid}"
                        error_log(error_message)

                # creating formwidget
                form_widget = FormWidget.objects.create(
                    screen_name_id=screen_obj.id,
                    card_size=12,
                    heading=screen,
                    formtable=table_obj,
                )
                # table obj is assign into list beacause below function or need list of table recods
                table_list = [table_obj]
                create_html_form(screen_obj)
                create_html_table(screen_obj,table_list)
                
                create_curd_view(screen_obj,table_list)
                create_form(screen_obj,table_list)
                create_serializer(screen_obj,table_list)
                create_model(screen_obj,table_list)
                create_api_curd_view(screen_obj,table_list)
                
                create_curd_url(screen_obj)
                create_api_curd_url(screen_obj)
                create_admin(screen_obj,table_list)
                create_footer(screen_obj)
            else:
                error_message=f"\n{screen} screen not found in ScreenDetailCSVs directory"
                error_log(error_message)
                print("doesn't exists")
 
        if count == 0:
            add_notcreated_modules(create_folder,sub_module)
    return True

def error_log(msg):
    print('erroe log start')
    error_file_path = 'D:\\BB Office\\GIT\\ERP-App-builder-V2\\projectserror_log.txt'
    with open(error_file_path, 'a') as error_file:
        error_file.write(msg)
    print('eroor log end')

def project_deletion(request):
    project_id = request.POST.get("selected_projects").split(',')
    print("project_id",project_id)
    try:
        for data in project_id:
            project_name = Project.objects.get(id = data)
            frontend_path = os.path.join(PROJECTS_FRONTEND, f'{project_name}_frontend')
            backend_path = os.path.join(PROJECTS_BACKEND, f'{project_name}_backend')
            import_project = os.path.join(IMPORT_PROJECTS_DETAILs, f'{project_name}_details')
            project_name.delete()
            if not os.path.exists(frontend_path):
                return HttpResponse(f"{frontend_path} doesn't exist")
            else:
                shutil.rmtree(frontend_path)
                
            if not os.path.exists(backend_path):
                return HttpResponse(f"{backend_path} doesn't exist")
            else:
                shutil.rmtree(backend_path)
                
            if not os.path.exists(import_project):
                print("this is not imported project")
            else:
                shutil.rmtree(import_project)
    except Exception as e:
        messages.success(
                request, 'close the related tabs')
            
    return redirect("create_project")