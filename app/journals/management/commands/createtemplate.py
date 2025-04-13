import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from journals.models import Template, User


class Command(BaseCommand):
    """Command to create default templates"""
    owner = User.objects.get(username=settings.DEFAULT_TEMPLATES_OWNER_USERNAME)
    help = "Create a new default template that will be added to templates.json"

    def handle(self, *args, **options):
        
        template_data = self._get_input_data_as_dict()
        self._create_template(template_data=template_data)
        self.add_new_template_to_default_templates(template_data=template_data)

    def add_new_template_to_default_templates(self, template_data):
        existing_templates = self._get_existing_templates()
        existing_templates = [template_data] + existing_templates
        print(existing_templates)
        self._write_to_templates_json_file(existing_templates)

    def _get_existing_templates(self):
        with open(settings.PATH_TO_TEMPLATES_JSON, "r") as template_file:
            return json.load(template_file)
        
    def _write_to_templates_json_file(self, template_list):
        with open(settings.PATH_TO_TEMPLATES_JSON, 'w') as template_file:
            json.dump(template_list, template_file, indent=2)
    
    def _create_template(self, template_data):
        Template.objects.create(
            owner=self.owner,
            name=template_data['template_name'],
            questions=template_data['questions']
        )

    def _get_input_data_as_dict(self):
        template_name = input("Enter the name of the default template: ")
        questions = input("Enter the questions separated by a (,): ").split(',')
        stripped_questions = [question.strip() for question in questions if question.strip()]

        template_data = {
            'template_name':template_name,
            'questions': stripped_questions
        }

        return template_data