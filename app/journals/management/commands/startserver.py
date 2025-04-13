"""Creates a new runserver command that checks if the default_templates_owner user exists,
    If they do not exist, create that user and assign
    the default templates to them
"""
import os
from os import environ
from django.core.management.commands.runserver import Command as BaseRunserverCommand
from django.conf import settings
from journals.models import Template, User
import json

class Command(BaseRunserverCommand):

    help = "Check if the default templates have been created before running server"
    def handle(self, *args, **options):
        if environ.get('RUN_MAIN') != 'true':
            self._check_for_default_models()
        super().handle(*args, **options)
        
        
                
    def _check_for_default_models(self):
        self.stdout.write(self.style.WARNING(f'CHECKING DATABASE FOR {settings.DEFAULT_TEMPLATES_OWNER_USERNAME}'))
        if not User.objects.filter(username=settings.DEFAULT_TEMPLATES_OWNER_USERNAME).exists():
            self.stdout.write(self.style.WARNING(f'{settings.DEFAULT_TEMPLATES_OWNER_USERNAME} NOT FOUND \nCREATING {settings.DEFAULT_TEMPLATES_OWNER_USERNAME}'))
            default_template_owner = self._set_up_database_with_default_user()   
        
        else:
            self.stdout.write(self.style.SUCCESS(f'{settings.DEFAULT_TEMPLATES_OWNER_USERNAME} FOUND'))
            default_template_owner = User.objects.get(username=settings.DEFAULT_TEMPLATES_OWNER_USERNAME)
        self._create_default_templates(default_template_owner)
    
        
    def _set_up_database_with_default_user(self):
        default_template_owner = User.objects.create_user(
            username= settings.DEFAULT_TEMPLATES_OWNER_USERNAME,
            first_name= 'All',
            last_name= 'All',
            email= 'all@journalsapp.com',
            password= 'DefaultUserAllPassword270224'
        )
        self.stdout.write(self.style.SUCCESS(f'{settings.DEFAULT_TEMPLATES_OWNER_USERNAME} WAS SUCCESSFULLY CREATED'))
        return default_template_owner
        
    
    def _create_default_templates(self, all_user):
        self.stdout.write(self.style.WARNING('CHECKING IF DEFAULT TEMPLATES HAVE BEEN CREATED'))
        default_templates = self._get_templates_from_json_file()
        for template in default_templates:
            if not Template.objects.filter(owner=all_user).filter(name=template['template_name']).exists():
                self.stdout.write(self.style.WARNING(f'TEMPLATE DOES NOT EXIST \nCREATING {template["template_name"]} TEMPLATE'))
                Template.objects.create(
                    name=template['template_name'],
                    owner=all_user,
                    questions=template['questions']
                )
        
        self.stdout.write(self.style.SUCCESS('ALL DEFAULT TEMPLATES EXIST'))

    def _get_templates_from_json_file(self):
        with open(settings.PATH_TO_TEMPLATES_JSON, "r") as template_file:
            return json.load(template_file)
