from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from journals.models import Journal, Entry, Template
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import tempfile
import shutil

class ViewEntryViewTestCase(TestCase):
    """Tests for viewing a specific entry."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = get_user_model().objects.get(username='@johndoe')
        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)
        self.template = Template.objects.create(name='Base Template')
        self.journal.template = self.template
        self.journal.save()
        self.entry = Entry.objects.create(journal=self.journal, entry_name='Test Entry')

    def test_view_entry_view(self):
   
        self.client.login(username=self.user.username, password='Password123')
        view_entry_url = reverse('view_entry', args=[self.journal.id, self.entry.id])

        response = self.client.get(view_entry_url)

        self.assertEqual(response.status_code, 200)


User = get_user_model()

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class EditEntryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        cls.template = Template.objects.create(name="Test Template", owner=cls.user, questions=["Q1"])
        cls.journal = Journal.objects.create(name="Test Journal", owner=cls.user, template=cls.template)
        cls.entry = Entry.objects.create(journal=cls.journal, entry_name="Test Entry")

    def setUp(self):
        self.client.login(username='testuser', password='testpass123')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tempfile.gettempdir(), ignore_errors=True)
        super().tearDownClass()

    def test_multimedia_file_upload(self):
        url = reverse('edit_entry', kwargs={'journal_id': self.journal.id, 'entry_id': self.entry.id})

        with open('media/test_images/test_image.jpeg', 'rb') as file:
            response = self.client.post(url, {
                'entry_name': 'Updated Entry Name',
                'mood': 'happy',
                'question_0': 'Answer 1',
                'multimedia_file': SimpleUploadedFile(file.name, file.read(), content_type='image/png'),
            })

        self.entry.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Check for redirect status code indicating success
        self.assertTrue(self.entry.multimedia_file, "The multimedia file was not saved.")
        filename = f"{slugify(self.entry.entry_name)}_"
        self.assertIn(filename, self.entry.multimedia_file.name, "The filename format didn't match the expectation.")