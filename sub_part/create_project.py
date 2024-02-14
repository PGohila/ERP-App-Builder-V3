from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Create a new Django project with main and sub-applications'

    def add_arguments(self, parser):
        parser.add_argument('project_name', type=str, help='Name of the project')
        parser.add_argument('location', type=str, help='Location for the project')

    def handle(self, *args, **options):
        project_name = options['project_name']
        location = options['location']

        # Create the Django project
        call_command('startproject', project_name, location)

        # Create main application
        call_command('startapp', 'mainapp', directory=f'{project_name}/mainapp')

        # Create sub-application
        call_command('startapp', 'subapp', directory=f'{project_name}/subapp')
