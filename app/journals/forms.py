"""Forms for the journals app."""
from django import forms
from django.db import models
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from journals.helpers import get_users_accessible_templates
from .models import User, Journal, Template, Entry, Profile
import os


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            
        )

        return user

    
class CreateNewJournal(forms.Form):
    journal_name = forms.CharField(label="Journal Name", max_length=50)
    template = forms.ModelChoiceField(queryset=Template.objects.none())  # Initialize with none

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs
        super(CreateNewJournal, self).__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['template'].queryset = get_users_accessible_templates(self.user) 

class CustomTemplateForm(forms.Form):
    journal_name = forms.CharField(label= 'Journal Name', 
                                                      max_length=50,                                                       
                                                      )

    template_name = forms.CharField(label= "Template Name", 
                                                       max_length=50)
    
    questions = forms.CharField(label= "Enter the questions you would like to answer in each entry of your journal. "
                                "Each question should be on a new line:", 
                                widget=forms.Textarea())
    
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super(CustomTemplateForm, self).__init__(*args, **kwargs)
        if not self.owner:
            raise forms.ValidationError("Must provide form with valid user")
    
    
    """Converts form input into a list, and removes whitespaces"""
    def clean_questions(self):
        questions = self.cleaned_data.get('questions')
        cleaned_questions = [question.strip() for question in questions.split('\n') if question.strip()]
        return cleaned_questions
    
    """With the given names, creates a new journal template and a new journal using said template"""
    def save(self):
        return self._create_new_template_and_journal_with_template()
    
    def _create_new_template_and_journal_with_template(self):
        cleaned_data = self._get_cleaned_data()
        new_custom_template = self._create_new_template(cleaned_data)
        new_journal_with_custom_template = self._create_new_journal_with_template(cleaned_data, new_custom_template)
        return new_journal_with_custom_template
        
    def _create_new_template(self, cleaned_data):
        template_name = cleaned_data.get('template_name')
        questions = cleaned_data.get('questions')
        return self._create_new_template_with_form_data(template_name=template_name, questions=questions)
    
    def _create_new_template_with_form_data(self, template_name, questions):
        new_custom_template = Template.objects.create(
            owner=self.owner,
            name=template_name,
            questions=questions
        )
        return new_custom_template
        
    
    def _create_new_journal_with_template(self, cleaned_data, new_custom_template):
        journal_name = cleaned_data.get('journal_name')
        new_journal_with_custom_template= Journal.objects.create(
            name= journal_name,
            owner=self.owner,
            template=new_custom_template
        )
        
        return new_journal_with_custom_template
    
    def _get_cleaned_data(self):
        if self.is_valid():
            return self.cleaned_data
        
class MoodTrackerForm(forms.Form):
    mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
   ]
    mood = forms.ChoiceField(label="Mood", choices=mood_choices)        


def validate_multimedia_file_extension(value):
    """ Multimediaformat validator """

    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp3', '.wav', '.mp4', '.avi', '.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_name', 'multimedia_file']

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        self.fields['mood'] = forms.ChoiceField(choices=MoodTrackerForm.mood_choices, label='Mood')
        self.fields['multimedia_file'].validators.append(validate_multimedia_file_extension)

        for i, question in enumerate(questions):
            # Initialize each form field for the corresponding question
            initial = ""
            try:
                initial = self.instance.responses[i]
            except IndexError:
                pass #This should set inital to "" but that is already done 
            
            self.fields[f'question_{i}'] = forms.CharField(
                    label=question,
                    required=False,
                    widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
                    initial=initial # Adjust the size by changing the rows and cols
                )


    def initial_responses(self, index):
        """Fetch initial response for a given question index, if any."""
        if self.instance.pk and self.instance.responses:  # Checks if the instance is saved and has responses
            try:
                return self.instance.responses[index]  # Attempt to get the response by index
            except IndexError:
                return ''  # If no response exists for this index, return an empty string
        return ''  # If instance is not saved or has no responses, return an empty string


    def save(self, commit=True):
        entry = super().save(commit=False)
        
        new_responses = [self.cleaned_data.get(f'question_{i}') for i, _ in enumerate(self.fields) if f'question_{i}' in self.cleaned_data]
        entry.responses = new_responses  
        if commit:
            entry.save()
        return entry


def validate_image_format(value):
    """ Validate file type """
    content_type = getattr(value, 'content_type', None)

    if not content_type:
        raise forms.ValidationError("Unable to determine the file's content type.")
    if content_type not in ['image/jpeg', 'image/png', 'image/gif']:
        raise forms.ValidationError("Invalid file format. Please upload an image in PNG, JPEG, or GIF format.")

class ProfilePicForm(forms.ModelForm):
    """Form to update Profile Picture"""

    profile_image = forms.ImageField(label="Profile Picture", validators=[
        FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'], message="Invalid file format. Please upload an image in PNG, JPEG, or GIF format."),
        validate_image_format,
    ])

    class Meta:
        """Form options"""
        model = Profile
        fields = ('profile_image', )

class SearchForm(forms.Form):
    """A general form for filtering models by name. """
    search_name = forms.CharField(max_length=50, required=False)
    
    def __init__(self, model, model_name_field, model_foreign_key=None, model_foreign_key_value=None, *args, **kwargs):
        self.model_to_filter = model
        
        if not isinstance(self.model_to_filter, type) or not issubclass(self.model_to_filter, models.Model):
            raise ValueError("Invalid model provided")
        if not self.model_to_filter:
            raise ValueError("No model provided to filter")
        
        self.model_name_field = model_name_field
        if not self.model_name_field:
            raise ValueError("No name field provided")
        
        """Check if model has a foreign key to be used or not"""
        self.model_foreign_key = model_foreign_key
        if self.model_foreign_key is not None:
            
            self.model_foreign_key_value = model_foreign_key_value
        
        super(SearchForm, self).__init__(*args, **kwargs)
    
    def get_filtered_results(self):
        if self.is_valid():
            search_filter = self._get_search_filter()
                
            return self.model_to_filter.objects.filter(**search_filter)
    
    def _get_search_filter(self):
        search_filter = {
                f"{self.model_name_field}__icontains": self.cleaned_data.get('search_name', ''),
                }
            
        if self.model_foreign_key:
            search_filter[self.model_foreign_key] = self.model_foreign_key_value
            
        return search_filter
                
        
    