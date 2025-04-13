from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from journals.models import User
from journals.models import Journal

class DeleteJournalViewTestCase(TestCase):
    """Tests of the delete journal view."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)

    def test_delete_journal(self):
        self.client.login(username=self.user.username, password="Password123")
        delete_url = reverse('delete_journal', args=[self.journal.id])
        response = self.client.post(delete_url) # POST request to delete journal
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Journal.objects.filter(id=self.journal.id).exists()) # Check journal is deleted

    def test_delete_journal_unauthenticated(self):
        delete_url = reverse('delete_journal', args=[self.journal.id])
        response = self.client.post(delete_url) 
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Journal.objects.filter(id=self.journal.id).exists()) # Check journal is not deleted

    def test_delete_journal_that_doesnt_exist(self):
        self.client.login(username=self.user.username, password="Password123")
        invalid_id = self.journal.id + 1
        delete_url = reverse('delete_journal', args=[invalid_id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)  # Check the repsonse code is not found (404)

