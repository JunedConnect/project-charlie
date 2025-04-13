from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from journals.models import Journal, Entry, Response, Template

class DownloadJournalPDFTestCase(TestCase):
    """Tests the download journal PDF view."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        base_template, _ = Template.objects.get_or_create(name='Base Template')
        

        self.journal = Journal.objects.create(name='Test Journal', owner=self.user,template=base_template)
        self.entry = Entry.objects.create(journal=self.journal, entry_name='Test Entry')
        self.entry.id = 1  # Set the entry ID to a specific number
        self.entry.save()  # Save the entry to ensure the ID is set

        Response.objects.create(entry=self.entry, question='Question 1', response='Response 1')
        Response.objects.create(entry=self.entry, question='Question 2', response='Response 2')

    def test_download_journal_pdf(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('download_journal_pdf', kwargs={'journal_id': self.journal.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_download_entry_pdf(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('download_entry_pdf', kwargs={'journal_id': self.journal.id, 'entry_id': self.entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    