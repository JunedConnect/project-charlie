from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from journals.models import Journal, Entry, Template


class EditEntryViewTestCase(TestCase):
    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='@johndoe')
        self.template = Template.objects.create(name='Base Template')

        self.journal = Journal.objects.create(name='Test Journal', owner=self.user, template=self.template)
        self.journal.save()
        self.entry = Entry.objects.create(journal=self.journal, entry_name='Test Entry')

    def test_edit_entry_view_with_multimedia_file(self):
        self.client.login(username=self.user.username, password='Password123')

        edit_entry_url = reverse('edit_entry', args=[self.journal.id, self.entry.id])

        image_file = SimpleUploadedFile("test_image.png", b"file_content", content_type="image/png")
        updated_entry_data = {
            'entry_name': 'Updated Entry',
            'multimedia_file': image_file,
        }

        response = self.client.post(edit_entry_url, updated_entry_data, format='multipart')
        self.assertEqual(response.status_code, 200)


    def test_edit_entry_view_without_multimedia_file(self):
       
        self.client.login(username=self.user.username, password='Password123')
        edit_entry_url = reverse('edit_entry', args=[self.journal.id, self.entry.id])
        updated_entry_data = {
            'entry_name': 'Updated Entry',
        }

        response = self.client.post(edit_entry_url, updated_entry_data)

        self.assertEqual(response.status_code, 200)
