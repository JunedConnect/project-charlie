from django.conf import settings
from django.shortcuts import redirect

from journals.models import Template, User

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def is_custom_template(template):
    default_template_owner = User.objects.get(username=settings.DEFAULT_TEMPLATES_OWNER_USERNAME)
    custom_template = Template.objects.filter(owner=default_template_owner).get(name=settings.CUSTOM_TEMPLATE_NAME)
    return template == custom_template

def redirect_to_custom_template_view(request, journal_name):
    session_data = {'journal_name': journal_name}
    session = request.session
    session.update(session_data)
    session.save()
    return redirect('custom_template')

def get_users_accessible_templates(user):
    return Template.objects.filter(owner=user) | Template.objects.filter(owner=User.objects.get(username=settings.DEFAULT_TEMPLATES_OWNER_USERNAME))
