from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date, timedelta
from django.db.models.signals import post_save
import uuid
from django.utils import timezone
from datetime import timedelta, date

# Dictionary of attainable achievements and levels

ACHIEVEMENT_LEVELS = {
    'Getting Started': 2,
    'Novice Scribe': 5,
    'Journal Enthusiast': 10,
    'Diary Keeper': 15,
    'Journal Master': 20,
    'Memoir Architect': 25,
    'Sage of Stories': 30,
    'Chronicle Champion': 40,
    'Legend of Literature': 50,
    'Pinnacle of Penmanship': 60,
    'Archivist Ascendant': 75,
    'Epic of Expression': 100,
}

mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('angry', 'Angry'),
   ]

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    recently_accessed_journals = models.JSONField(default=list, blank=True, null=True)  
    
    

    class Meta:
        """Model options."""
        ordering = ['last_name', 'first_name']

    def get_journals_without_today_entry(self):
        journals = self.get_associated_journals()
        journals_without_today_entry = [journal.id for journal in journals if not journal.check_if_today_entry_exists()]
        return journals.filter(id__in= journals_without_today_entry)
    
    def get_user_today_entries(self):
        journals = self.get_associated_journals()
        today_entries = Entry.objects.filter(journal__in=journals, date=date.today())
        return today_entries
        
    
    def add_to_journals_recently_accessed(self, journal):
        """This treats the JSONField as a set of size 3"""
        journal_id = journal.id
        if journal_id in self.recently_accessed_journals:
            self.recently_accessed_journals.remove(journal_id)
        if len(self.recently_accessed_journals) == 4:
            self.recently_accessed_journals.pop(3)
        
        self.recently_accessed_journals = [journal.id] + self.recently_accessed_journals
        self.save()  # Don't forget to save the model to persist changes
        
    def get_recently_accessed_journals(self):
        return [Journal.objects.get(id=journal_id,) for journal_id in self.recently_accessed_journals]

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def get_associated_journals(self): 
        """Returns a list of all of the user's journals."""
        return Journal.objects.filter(owner=self)
    
    def has_logged_in_last_24_hours(self):
        """Determined if user has logged in within last 24 hours"""
        
        # If the user has never logged in return False
        if self.last_login is None:
            return False
        
        # Calculate time difference since last login
        time_since_last_login = timezone.now() - self.last_login
        
        #Check if last login is within the last 24 hours
        return time_since_last_login <= timedelta(days=1)


class Achievement(models.Model):
    """ Achievemnt model for gamification """
    name = models.CharField(max_length=255)
    description = models.TextField()
    level = models.PositiveIntegerField(default=0) 
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Define achievement name mapping """

        self.level = ACHIEVEMENT_LEVELS.get(self.name, 0)
        super(Achievement, self).save(*args, **kwargs)

def profile_image_upload_path(instance, filename):
        """Generate unique filename for profile images"""
        
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return f"images/{filename}"

class Profile(models.Model):
    """Create A User Profile Model for additional User fields not used in authentication"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to=profile_image_upload_path)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, blank=True)


    def __str__(self):
        """Displays username in admin view"""
        return self.user.username

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.required_experience_for_next_level():
            self.level_up()
        self.save()

    def level_up(self):
        self.experience -= self.required_experience_for_next_level()
        self.level += 1
        self.save()
        self.check_and_assign_achievements()

    def required_experience_for_next_level(self):
        return self.level * 50

    def check_and_assign_achievements(self):
        for name, level in ACHIEVEMENT_LEVELS.items():
            if self.level >= level:
                achievement, created = Achievement.objects.get_or_create(
                    name=name,
                    defaults={'description': f'Reached level {self.level} in journaling!'}
                )
                self.achievements.add(achievement)

    def highest_achievement(self):
        return self.achievements.order_by('-level').first()

# Create Profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
post_save.connect(create_profile, sender=User)

    
class Journal(models.Model):
    name = models.CharField(max_length=50) 
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='journals')
    template = models.ForeignKey('Template', on_delete=models.SET_NULL, null=True, related_name='journals')
    date = models.DateField(auto_now_add=True)

    def set_name(self, newName):
        self.name = newName
    
    def get_date_of_journal_creation(self):
        return self.date
    
    def get_entries(self):
        return Entry.objects.filter(journal=self)

    def get_number_of_entries(self):
        return self.get_entries().count()
    
    
    def __str__(self):
        return self.name

    def get_name_without_whitespace(self):
        return self.name.replace(" ", "")
    
    def check_if_today_entry_exists(self):
        return Entry.objects.filter(journal=self, date=date.today()).exists()
        
        
    def get_streak(self):
        entries = self.entries.order_by('-date')
        if not entries.exists():
            return 0

        # Check if there's an entry for today
        today = timezone.now().date()
        has_entry_today = entries.filter(date=today).exists()

        # If there's no entry for today, start counting from yesterday
        current_date = today if has_entry_today else today - timedelta(days=1)

        streak = 0
        for entry in entries:
            if entry.date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif streak > 0:
                # If a streak has started but the next entry doesn't match the expected date
                break

        return streak


class Entry(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')
    entry_name = models.CharField(max_length=50, default='New Entry')
    date = models.DateField(auto_now_add=True)
    responses = models.JSONField(default=list)  # Store responses as a dictionary
    mood = models.CharField(max_length=50, null=True, blank=True)  # New field for mood tracking
    multimedia_file = models.FileField(upload_to='multimedia/', null=True, blank=True)

    def get_date(self):
        return self.date
     
    

class Template(models.Model):
    name = models.CharField(max_length=50, default='Template Name')
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='templates')
    questions = models.JSONField(default=list)  # Use default=list to default to an empty list

    def get_questions(self):
        """Returns the list of questions."""
        return self.questions

    def add_question(self, question):
        """Adds a question to the questions list."""
        if not self.questions:
            self.questions = []
        self.questions.append(question)
        self.save()  # Don't forget to save the model to persist changes

    def set_questions(self, questions):
        """Sets the questions list to a new list of questions."""
        self.questions = questions
        self.save()  # Persist changes to the database

    def __str__(self):
        return self.name

class Response(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    response = models.TextField()

    def __str__(self):
        return f"Response: {self.question}"