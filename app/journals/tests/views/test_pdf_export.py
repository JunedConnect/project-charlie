from django.test import TestCase, Client
from django.urls import reverse
from journals.models import User, Journal, Entry, Template
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.dateparse import parse_date

class PDFExportTest(TestCase):


    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='@testuser', password='testpassword', email='test@test.com')
        self.another_user, _ = User.objects.get_or_create(username='@anotheruser', defaults={'password': 'password123', 'email': 'another@example.com'})
        self.another_user.set_password('password123')
        self.another_user.save()
        self.template = Template.objects.create(name='Test Template', owner=self.user, questions=['Q1?', 'Q2?'])
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user, template=self.template)
        self.entry = Entry.objects.create(
            journal=self.journal,
            entry_name='Test Entry',
            date=parse_date("2024-01-01"),
            mood='happy',
            responses=['A1', 'A2']
        )

        self.client.login(username='@testuser', password='testpassword')

        # Create test pdf content
        self.test_pdf_content = BytesIO()
        self.test_pdf_content.write(b'%PDF-1.4 Test PDF')
        self.test_pdf_content.seek(0)

    def test_entry_pdf_export(self):
        download_url = reverse('download_entry_pdf', args=[self.journal.pk, self.entry.pk])
        
        # Trigger the view to generate the PDF
        response = self.client.get(download_url)
        
        # Check that the response is a PDF and is delivered successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_journal_pdf_export(self):
        download_url = reverse('download_journal_pdf', args=[self.journal.pk])
        
        response = self.client.get(download_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_export_permission(self):
        self.client.logout()
        
        # Ensure the user is logged out and then log in as another user
        self.client.login(username='@anotheruser', password='password123')
        
        # Confirm another_user does not own the journal or entry
        self.assertNotEqual(self.journal.owner, self.another_user)
        self.assertNotEqual(self.entry.journal.owner, self.another_user)

        entry_download_url = reverse('download_entry_pdf', args=[self.journal.pk, self.entry.pk])
        journal_download_url = reverse('download_journal_pdf', args=[self.journal.pk])

        # Unauthorised PDF access
        entry_response = self.client.get(entry_download_url)
        journal_response = self.client.get(journal_download_url)

        # Check for redirects indicating lack of access
        self.assertEqual(entry_response.status_code, 302, "Expected a redirect due to permission issue.")
        self.assertEqual(journal_response.status_code, 302, "Expected a redirect due to permission issue.")
        self.assertRedirects(entry_response, expected_url=reverse('journals_home'), fetch_redirect_response=False)
        self.assertRedirects(journal_response, expected_url=reverse('journals_home'), fetch_redirect_response=False)

        # Log in as the correct user
        self.client.logout()
        self.client.login(username='@testuser', password='testpassword')
        entry_response = self.client.get(entry_download_url)
        journal_response = self.client.get(journal_download_url)

        self.assertEqual(entry_response.status_code, 200)
        self.assertEqual(journal_response.status_code, 200)
