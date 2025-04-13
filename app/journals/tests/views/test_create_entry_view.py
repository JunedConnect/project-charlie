from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from journals.models import Journal, Entry, Response, Template
from django.contrib.messages import get_messages 

class CreateEntryViewTestCase(TestCase):
    """Tests for creating a new entry."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='@johndoe')
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)

        self.template = Template.objects.create(name='Base Template')
        self.journal.template = self.template
        self.journal.save()

    def test_create_entry_view(self):
        self.client.login(username=self.user.username, password='Password123')

        entry_data = {
            'entry_name': 'New Entry', 
            'responses': ['Response 1', 'Response 2'], 
            'mood': 'happy'  # Mood
        }

        create_entry_url = reverse('create_entry', args=[self.journal.id])

        today_entry = Entry.objects.create(journal=self.journal, entry_name="Today's Entry")
        response = self.client.post(create_entry_url, entry_data)
       
        self.assertRedirects(response, reverse('view_journal_entries', args=[self.journal.id]))

        today_entry.delete()
        response = self.client.post(create_entry_url, entry_data)
     
        self.assertEqual(response.status_code, 302) 
    
    def test_create_entry_view_get(self):
      
        self.client.login(username=self.user.username, password='Password123')

        create_entry_url = reverse('create_entry', args=[self.journal.id])

        response = self.client.get(create_entry_url)

        self.assertEqual(response.status_code, 302)

    def test_create_entry_view_get_today_entry_exists(self):
        self.client.login(username=self.user.username, password='Password123')

        Entry.objects.create(journal=self.journal, entry_name="Today's Entry")
        create_entry_url = reverse('create_entry', args=[self.journal.id])

        response = self.client.get(create_entry_url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Entry could not be created. You have already created one today!")

        self.assertEqual(response.url, reverse('view_journal_entries', args=[self.journal.id]))
