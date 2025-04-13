import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from journals.forms import CustomTemplateForm, LogInForm, PasswordForm, SearchForm, UserForm, SignUpForm, ProfilePicForm
from journals.helpers import is_custom_template, login_prohibited, redirect_to_custom_template_view
from journals.models import Journal, Entry, Profile
from journals.forms import CreateNewJournal, EditEntryForm, MoodTrackerForm
from django.views.generic import DetailView

from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.shortcuts import get_object_or_404
from journals.models import Entry, Journal
import io
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Image
from django.utils import timezone

from reportlab.lib.styles import getSampleStyleSheet

from django.utils.text import slugify
import uuid

@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')

mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
   ]
class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class JournalAndEntryAccessMixin(AccessMixin):
   
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            # Redirect unauthenticated users to login page
            login_url = reverse('log_in')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")

        entry_id = kwargs.get('entry_id')
        journal_id = kwargs.get('journal_id')
        journal = None

        # Check if entry exists
        if entry_id:
            entry = get_object_or_404(Entry, id=entry_id)
            journal = entry.journal

        # Verify if journal_id exists
        elif journal_id:
            journal = get_object_or_404(Journal, id=journal_id)

        if journal and request.user != journal.owner:
            return HttpResponseRedirect(reverse('journals_home'))

        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, View):
    """Display the current user's dashboard."""
    http_method_names = ['get']
    template_name = 'dashboard.html'

    def get(self, request):
        current_user = self.request.user
        profile = Profile.objects.get(user=current_user)
        recently_accessed_journals = current_user.get_recently_accessed_journals()
        experience_needed = profile.required_experience_for_next_level()
        progress_to_next_level = (profile.experience / experience_needed) * 100 if experience_needed > 0 else 0
        
        top_users = Profile.objects.order_by('-level', '-experience')[:10]
        in_top_users = profile in top_users

        # Calculate rank if not in top_users
        if not in_top_users:
            all_profiles = Profile.objects.order_by('-level', '-experience')
            ranks = {profile.id: rank for rank, profile in enumerate(all_profiles, start=1)}
            current_user_rank = ranks.get(profile.id)
        else:
            current_user_rank = None

        context = {
            'user': current_user,
            'journal_list': recently_accessed_journals,
            'level': profile.level,
            'current_experience': profile.experience,
            'experience_needed': experience_needed,
            'progress_to_next_level': progress_to_next_level,
            'achievements': profile.achievements.all(),
            'top_users': top_users,
            'in_top_users': in_top_users,
            'current_user_rank': current_user_rank,
        }
        
        return render(self.request, 'dashboard.html', context)
    
class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')




class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

class JournalsView(LoginRequiredMixin, View):
    """Display the user's journals"""
    template_name = 'journals_base.html'
    http_method_names = ['get']
    def get(self,request):
        journal_list = request.user.get_associated_journals()
        return render(request, "journals_base.html", {"journal_list": journal_list})

class EntriesView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    """Display the journals entries"""
    template_name = 'entries_base.html'
    http_method_names = ['get', 'post']
    def get(self,request,journal_id):
        
        journal = Journal.objects.get(id=journal_id)
        entry_list = journal.get_entries()
        self.request.user.add_to_journals_recently_accessed(journal)
        streak = journal.get_streak()
        form = SearchForm(
            model=Entry,
            model_name_field="entry_name",
            model_foreign_key="journal",
            model_foreign_key_value=journal
        )
      
        return render(request, 'view_journal_entries.html', {"form": form, "entry_list": entry_list, 'journal': journal})

    def post(self, request, journal_id):
        journal = Journal.objects.get(id=journal_id)
        form = SearchForm(
            model=Entry,
            model_name_field="entry_name",
            model_foreign_key="journal",
            model_foreign_key_value=journal,
            data=self.request.POST
        )
        
        entry_list = form.get_filtered_results()
        return render(request, 'view_journal_entries.html', {"form": form, "entry_list": entry_list, 'journal': journal})

class CreateJournalView(LoginRequiredMixin, View):
    """Display the create_journal screen and handle journal creations"""
    template_name = 'create_journal.html'
    http_method_names = ['get', 'post']
    def get(self,request):
        form = CreateNewJournal(user=request.user)
        journal_list = request.user.get_associated_journals()
        return render(request, "create_journal.html", {"form": form, "journal_list": journal_list})

    def post(self,request):
        form = CreateNewJournal(request.POST, user=request.user)
        if form.is_valid():
            j_name = form.cleaned_data["journal_name"]
            j_template = form.cleaned_data["template"]
            if is_custom_template(j_template):
                return redirect_to_custom_template_view(request=request, journal_name=j_name)
            j = Journal.objects.create(name=j_name, owner=request.user, template=j_template)

            messages.add_message(self.request, messages.SUCCESS, "Journal created!")
        else:
            messages.add_message(self.request, messages.ERROR, "Journal could not be created.")

        return redirect(reverse(settings.JOURNAL_HOME_URL))
    

class CustomTemplateView(LoginRequiredMixin, View):
    template_name = 'custom_template.html'
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        form = self._create_form_with_initial_data()
        return render(self.request, 'custom_template.html', {"form": form})
    
    def _get_journal_name(self):
        journal_name = self.request.session.get('journal_name', None)
        if journal_name is None:
            journal_name = self._create_journal_name_when_name_is_not_stored_in_session()
        return journal_name

    def _create_journal_name_when_name_is_not_stored_in_session(self):
        user_new_journal_count = self._count_user_journals_that_begin_with_new_journal()
        journal_name = f"New Journal #{user_new_journal_count}"
        return journal_name

    def _count_user_journals_that_begin_with_new_journal(self):
        user_journals = Journal.objects.filter(owner=self.request.user)
        user_new_journal_count = user_journals.filter(name__startswith='New Journal').count()
        return user_new_journal_count
    
    def _create_form_with_initial_data(self):
        journal_name = self._get_journal_name()
        initial_form_values = {'journal_name': journal_name}
        return CustomTemplateForm(owner=self.request.user, initial=initial_form_values)

    def post(self, request, *args, **kwargs):
        form = self._create_form_from_post_data()
        return self._validate_form(form)

    
    def _get_form_data(self):
        form_data = self.request.POST.copy()
        form_data['journal_name'] = form_data.get('journal_name', None) or self.request.session.get('journal_name') 
        form = CustomTemplateForm(form_data, owner=self.request.user)
        return form_data

    def _create_form_from_post_data(self):
        form_data = self._get_form_data()
        form = CustomTemplateForm(form_data, owner=self.request.user)
        return form
    
    def _save_form(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, f"Custom Template '{form.cleaned_data.get('template_name')}' has been saved")
        if self.request.session.get('journal_name', None):
            del self.request.session['journal_name']
        return self._redirect_to_journal_home()
        
    def _redirect_to_journal_home(self):
        return redirect(reverse(settings.JOURNAL_HOME_URL))
    
    def _reject_form(self, form):
        messages.add_message(self.request, messages.ERROR, "Template could not be created")
        return render(self.request, 'custom_template.html', {'form': form})
    
    def _validate_form(self, form):
        if form.is_valid():
            return self._save_form(form=form)
        else:            
            return self._reject_form(form=form)

class CreateEntryView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    """Display the journals entries"""
    template_name = 'entries_base.html'
    http_method_names = ['get', 'post']

    def get(self, request, journal_id):
        journal = Journal.objects.get(id=journal_id)
        if Journal.check_if_today_entry_exists(journal):
            messages.add_message(request, messages.ERROR, "Entry could not be created. You have already created one today!")
            return redirect('view_journal_entries', journal_id=journal.id)
        else:
            entry = Entry.objects.create(journal=journal, entry_name=f"New Entry #{Entry.objects.filter(journal=journal).filter(entry_name__startswith='New Entry').count()}")
            return redirect('edit_entry', journal_id=journal.id, entry_id=entry.id)

    def post(self, request, journal_id):
        journal = Journal.objects.get(id=journal_id)
        if Journal.check_if_today_entry_exists(journal):
            messages.add_message(request, messages.ERROR, "Entry could not be created. You have already created one today!")
            return redirect('view_journal_entries', journal_id=journal.id)
        else:
            entry = Entry.objects.create(journal=journal, entry_name=f"New Entry #{Entry.objects.filter(journal=journal).filter(entry_name__startswith='New Entry').count()}")
            return redirect('edit_entry', journal_id=journal.id, entry_id=entry.id)


class EditEntryView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    template_name = 'edit_entry.html'
    http_method_names = ['get', 'post']

    def get(self, request, journal_id, entry_id):
        journal = Journal.objects.get(id=journal_id)
        entry = get_object_or_404(Entry, id=entry_id, journal__owner=request.user) 

        form = EditEntryForm(instance=entry, questions=journal.template.questions)  
        
        initial_mood = entry.mood if hasattr(entry, 'mood') else None
        mood_form = MoodTrackerForm(initial={'mood': initial_mood})
        
        return render(request, self.template_name, {'form': form, 'entry': entry, 'journal': journal, 'mood_form': mood_form})
    
    def post(self, request, journal_id, entry_id):
        journal = Journal.objects.get(id=journal_id)

        entry = get_object_or_404(Entry, id=entry_id, journal__owner=request.user)  
        form = EditEntryForm(request.POST, instance=entry, questions=entry.journal.template.questions)  
        form = EditEntryForm(request.POST, request.FILES, instance=entry, questions=entry.journal.template.questions) # Pass questions for form generation

        if form.is_valid():
            entry = form.save(commit=False)

            multimedia_file = request.FILES.get('multimedia_file')
            if multimedia_file:
                # Check if the file is an image
                if 'image' in multimedia_file.content_type:
                    file_extension = '.png'  # Assume PNG for images
                elif 'video' in multimedia_file.content_type:
                    file_extension = '.mp4'
                else:
                    # Handle other file types if needed
                    file_extension = ''

                # Generate a unique filename
                filename = f"{slugify(entry.entry_name)}_{str(uuid.uuid4())[:8]}{file_extension}"
                entry.multimedia_file.save(filename, multimedia_file)

            entry.save()

            mood_form = MoodTrackerForm(request.POST)
            if mood_form.is_valid():
                mood = mood_form.cleaned_data['mood']
                entry.mood = mood
                entry.save()
 
            messages.add_message(request, messages.SUCCESS, "Entry updated successfully!")
            return redirect('view_journal_entries', journal_id=journal_id)
        else:
            messages.add_message(request, messages.ERROR, "Unable to update entry.")
            mood_form = MoodTrackerForm(request.POST) 
            return render(request, self.template_name, {'form': form, 'entry': entry, 'journal': journal, 'mood_form': mood_form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def form_valid(self, form):
        # Handle UserForm update
        self.object = form.save()

        # Handle ProfilePicForm update
        profile_form = ProfilePicForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        if profile_form.is_valid():
            profile_form.save()

        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile Updated!")
        return redirect(reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class DeleteJournalView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    """Handle deletion of a journal via POST request"""
    http_method_names = ['post']  

    
    def post(self, request, journal_id):
        journal = get_object_or_404(Journal, id=journal_id)
        # Check if the current user owns the journal
        if request.user == journal.owner:
            journal.delete()
            if journal_id in self.request.user.recently_accessed_journals:
                self.request.user.recently_accessed_journals.remove(journal_id)
                self.request.user.save()

            messages.add_message(self.request, messages.SUCCESS, "Journal deleted!")
        else:
            messages.add_message(self.request, messages.ERROR, "You are not authorized to delete this journal.")
        
        return redirect(reverse(settings.JOURNAL_HOME_URL))


class DeleteEntryView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    """Handle deletion of a journal entry via POST request"""
    http_method_names = ['post']  
    def post(self, request, entry_id):
        entry = get_object_or_404(Entry, id=entry_id)
        # Check if the current user owns the journal and entry is part of said journal
        if request.user == entry.journal.owner:
            entry.delete()
            messages.add_message(self.request, messages.SUCCESS, "Entry deleted!")
        else:
            messages.add_message(self.request, messages.ERROR, "You are not authorized to delete this entry.")

        return redirect('view_journal_entries', journal_id=entry.journal.id)

class EntryDetailView(JournalAndEntryAccessMixin, DetailView):
    """Display an individual entry"""
    model = Entry
    template_name = 'entry_detail.html'
    context_object_name = 'entry'

class ViewEntryView(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    """Display the specific entry"""
    template_name = 'view_entry.html'
    
    def get(self, request, journal_id, entry_id):
        journal = get_object_or_404(Journal, id=journal_id)
        entry = get_object_or_404(Entry, id=entry_id, journal=journal)  # Ensure entry belongs to journal
        multimedia_file = entry.multimedia_file

        # Assuming each response in entry.responses aligns by index with a question in journal.template.questions
        questions_and_responses = zip(journal.template.questions, entry.responses)

        return render(request, 'view_journal_entry.html', {
            "entry": entry,
            'journal': journal,
            'questions_and_responses': questions_and_responses,
            'multimedia_file': multimedia_file, 
        })

class DownloadEntryPDF(LoginRequiredMixin, JournalAndEntryAccessMixin, View):
    def get(self, request, journal_id, entry_id):

        journal = get_object_or_404(Journal, id=journal_id)
        entry = get_object_or_404(Entry, id=entry_id, journal=journal)

        title = entry.entry_name
        date = entry.date
        mood = entry.mood
        questions_and_responses = list(zip(journal.template.questions, entry.responses))

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
   
        styles = getSampleStyleSheet()
        NormalTextStyle = styles['Normal']

        title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16)
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {date}", NormalTextStyle))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Mood: {mood}", NormalTextStyle))
        elements.append(Spacer(1, 12))

        

        data = [['Question', 'Response']]
        for question, response in questions_and_responses:
            data.append([question, response])

        

        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)

        if entry.multimedia_file:

            _, file_extension = os.path.splitext(entry.multimedia_file.name)

            if file_extension.lower() != ".mp4":
                elements.append(Spacer(1, 20))
                elements.append(Image(entry.multimedia_file.path, width=300, height=300))
                elements.append(Spacer(1, 20))
                        
        doc.build(elements)

        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="entry_{entry_id}.pdf"'

        return response

class PDFGeneratorMixin:
    def generate_pdf(self, elements, filename):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        doc.build(elements)

        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    def add_entry_details(self, elements, entry):
        title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16)
        elements.append(Paragraph(entry.entry_name, title_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Date: {entry.date}", self.normal_text_style()))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Mood: {entry.mood}", self.normal_text_style()))
        elements.append(Spacer(1, 12))

        data = [['Question', 'Response']]
        for question, response in zip(entry.journal.template.questions, entry.responses):
            data.append([question, response])

        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        if entry.multimedia_file:
            _, file_extension = os.path.splitext(entry.multimedia_file.name)
            if file_extension.lower() != ".mp4":
                elements.append(Spacer(1, 20))
                elements.append(Image(entry.multimedia_file.path, width=300, height=300))
                elements.append(Spacer(1, 20))

    def normal_text_style(self):
        styles = getSampleStyleSheet()
        return styles['Normal']


class DownloadEntryPDF(LoginRequiredMixin, PDFGeneratorMixin, JournalAndEntryAccessMixin, View):
    def get(self, request, journal_id, entry_id):
        journal = get_object_or_404(Journal, id=journal_id)
        entry = get_object_or_404(Entry, id=entry_id, journal=journal)

        elements = []
        self.add_entry_details(elements, entry)

        return self.generate_pdf(elements, f'entry_{entry_id}.pdf')


class DownloadJournalPDF(LoginRequiredMixin, PDFGeneratorMixin, JournalAndEntryAccessMixin, View):
    def get(self, request, journal_id):
        journal = get_object_or_404(Journal, id=journal_id)
        entries = Entry.objects.filter(journal=journal)
        journal_title = journal.name

        elements = [Paragraph(journal_title, self.normal_text_style()), Spacer(1, 12)]

        for entry in entries:
            self.add_entry_details(elements, entry)
            elements.append(Spacer(1, 24))  # Add some space between entries

        return self.generate_pdf(elements, f'journal_{journal_id}_entries.pdf')