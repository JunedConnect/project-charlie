from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from journals.models import User
from journals.models import Journal, Entry
from journals.tests.helpers import reverse_with_next

class DeleteEntryViewTestCase(TestCase):
    """Tests of the delete entry view."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)
        self.entry = Entry.objects.create(journal=self.journal, entry_name='New Entry', responses=['Entry body'])

    def test_delete_entry_view(self):
        self.client.login(username=self.user.username, password="Password123")
        delete_url = reverse('delete_entry', args=[self.entry.id]) 
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())

    def test_delete_entry_view_unauthenticated(self):
        delete_url = reverse('delete_entry', args=[self.journal.id])
        response = self.client.post(delete_url) # POST request to delete journal (unauthenticated)
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertTrue(Journal.objects.filter(id=self.journal.id).exists())

    def test_delete_entry_that_doesnt_exist(self):
        self.client.login(username=self.user.username, password="Password123")
        invalid_id = self.journal.id + 1
        delete_url = reverse('delete_entry', args=[invalid_id])
        response = self.client.post(delete_url) 
        self.assertEqual(response.status_code, 404) 
    
