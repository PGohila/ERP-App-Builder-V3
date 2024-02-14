from.models import *
import re
import os
import csv
from .constant import *


def error_log(msg):
    print('erroe log start')
    error_file_path = 'D:\Projects\App Bulider\Excel import\ERP-app-builder\error_log.txt'
    with open(error_file_path, 'a') as error_file:
        print('error_file',error_file)
        error_file.write(msg)
    print('eroor log end')

def space_to_underscore(string):
    if isinstance(string, str):
        result = re.sub(r'^[^a-zA-Z0-9_]+', '', string)
        result = result.replace(" ", "_")
        return result
    else:
        return string

def field_name_validate(string,table_id):
    start_with = str(string).lower().startswith(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'))
    fields = Field.objects.filter(table_id = table_id,field_name=string)
    if start_with and not fields.exists() and string != 'id':
        return True
    else:
        return False
    
def validate_field_type(field_type):
    try:
        field_type_list =  ['CharField', 'IntegerField', 'BooleanField', 'DateField', 'DateTimeField',
                'FileField', 'FloatField','DecimalField', 'ForeignKey', 'GenericIPAddressField', 'ImageField', 
                'ManyToManyField', 'OneToOneField', 'TextField', 'TimeField']
        if field_type in field_type_list:
            return True
        else:
            return False
    except:
        return False


def remove_special_characters(input_string):
    if isinstance(input_string, str):
        # Define a regular expression pattern to match special characters
        pattern = r'[^a-zA-Z0-9\s]+'  # Match special characters except spaces

        # Use the sub() function to replace special characters with an empty string
        cleaned_string = re.sub(pattern, '_', input_string)

        # Replace consecutive spaces with a single underscore
        cleaned_string = re.sub(r'\s+', '_', cleaned_string)

        result = re.sub(r'(?<!_)([A-Z])', r'_\1', cleaned_string)
        # Trim underscores at the beginning and end of the string
        cleaned_string = result.strip('_')

        return cleaned_string
    else:
        return input_string
    
def model_id_generation(pre,count):
    uniqueid = pre + str(count)
    check_model_id = Model_Identification.objects.filter(model_id=uniqueid).exists()
    if check_model_id:
        model_id_generation(pre,count + 1)
    else:
        return uniqueid
    
def model_name_generation(pre,count,projectid):
    uniquename = pre + str(count)
    check_model_name = Model_Identification.objects.filter(project_id = projectid,model_name=uniquename).exists()
    if check_model_name:
        model_name_generation(pre,count+1)
    else:
        return uniquename
    
def create_folder_and_csv(projectid):
    # Define the folder name
    project_name = Project.objects.get(id = projectid)
    folder_name = f'{project_name}_details'
    
    # Get the path where you want to create the folder
    folder_path = os.path.join(IMPORT_PROJECTS_DETAILs, folder_name)  # Assuming you want to create a folder at the root of your project
    try:
        # Create the folder
        os.makedirs(folder_path)
        # create another folder for created table details
        folder_path1 = os.path.join(folder_path,"Tables_details")
        os.makedirs(folder_path1)
        # Create a CSV file within the folder
        csv_filename = os.path.join(folder_path, 'screenslist.csv')
        notcreated_module = os.path.join(folder_path, 'notcreated_module.csv')
        with open(notcreated_module, 'w', newline='') as csvfile1:
            csv_writer1 = csv.writer(csvfile1)
            csv_writer1.writerow(['Sub Module'])
          # Example data
        screenlist_csvpath = csv_filename
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Main Module', 'Sub Module', 'Screens'])  # Write header row
    except FileExistsError:
        csv_filename = os.path.join(folder_path, 'screenslist.csv')
        screenlist_csvpath = csv_filename
        message = "Folder already exists!"
    return folder_path

def  listing_created_screen(csv_path,screen,submenu):
    csv_filename = os.path.join(csv_path, 'screenslist.csv')
    with open(csv_filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # Write header row
        csv_writer.writerow([' ', f'{submenu}', f'{screen}'])
    screen_name = screen
    return screen_name

def create_tables_files(table_name,projectid):
    project_name = Project.objects.get(id = projectid)
    folder_name = f'{project_name}_details'
    IMPORT_PROJECTS_DETAILs = os.path.abspath(f"projects/Project_Details/{folder_name}/Tables_details/")
    folder_path = os.path.join(IMPORT_PROJECTS_DETAILs, f'{table_name}.csv')
    with open(folder_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Field Name'])  # Assuming you want to create a folder at the root of your project
    return folder_path

def add_fields_csv(tablefile_path,field_name):
    with open(tablefile_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # Write header row
        csv_writer.writerow([f'{field_name}'])
    message = "successfully created"
    return message

def add_notcreated_modules(csv_path,sub_module):
    csv_filename = os.path.join(csv_path, 'notcreated_module.csv')
    with open(csv_filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile) # Write header row
        csv_writer.writerow([f'{sub_module}'])
    message = "successfully created"
    return message
