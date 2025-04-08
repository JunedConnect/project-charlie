from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from journals.models import Journal, Entry, Template

class EditEntryViewTestCase(TestCase):
    """Tests for editing an entry."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='@johndoe')
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)
        self.template = Template.objects.create(name='Base Template') 
        self.journal.template = self.template
        self.journal.save()
        self.entry = Entry.objects.create(journal=self.journal, entry_name='Test Entry')


    def test_edit_entry_view_get(self):
      
        self.client.login(username=self.user.username, password='Password123')
        edit_entry_url = reverse('edit_entry', args=[self.journal.id, self.entry.id])

        response = self.client.get(edit_entry_url)
        self.assertEqual(response.status_code, 200)


    def test_edit_entry_view_post(self):
        self.client.login(username=self.user.username, password='Password123')

        edit_entry_url = reverse('edit_entry', args=[self.journal.id, self.entry.id])

        updated_entry_data = {
            'entry_name': 'Updated Entry',
        }

        updated_entry_data['mood'] = 'happy'

        response = self.client.post(edit_entry_url, updated_entry_data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Entry updated successfully!")

    def test_edit_entry_view_post_failure_case(self):
        self.client.login(username=self.user.username, password='Password123')

        edit_entry_url = reverse('edit_entry', args=[self.journal.id, self.entry.id])

        updated_entry_data = {
            'entry_name': 'Updated Entry',
        }

        response = self.client.post(edit_entry_url, updated_entry_data)
        self.assertEqual(response.status_code, 200)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Unable to update entry.")


