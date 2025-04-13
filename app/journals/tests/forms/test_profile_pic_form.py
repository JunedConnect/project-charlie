from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from journals.forms import ProfilePicForm
from journals.models import Profile
from django import forms

class ProfilePicFormTestCase(TestCase):
    """Unit tests for the profile picture form."""

    fixtures = [
        'journals/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.image_path = 'media/test_images/test_image.jpeg'  # Path to a sample image file for testing
        self.invalid_image_path = 'media/test_images/invalid_image.txt'  # Path to an invalid image file for testing

    def test_form_has_necessary_fields(self):
        form = ProfilePicForm()
        self.assertIn('profile_image', form.fields)
        profile_image_field = form.fields['profile_image']
        self.assertTrue(isinstance(profile_image_field, forms.ImageField))

    def test_valid_profile_pic_form(self):
        with open(self.image_path, 'rb') as image_file:
            image = SimpleUploadedFile('test_image.jpeg', image_file.read(), content_type='image/jpeg')
            form = ProfilePicForm(files={'profile_image': image})
            self.assertTrue(form.is_valid())

    def test_invalid_profile_pic_form_invalid_format(self):
        with open(self.invalid_image_path, 'rb') as invalid_file:
            invalid_image = SimpleUploadedFile('invalid_image.txt', invalid_file.read(), content_type='text/plain')
            form = ProfilePicForm(files={'profile_image': invalid_image})
            self.assertFalse(form.is_valid())
            self.assertIn('profile_image', form.errors)
            self.assertIn('Upload a valid image. The file you uploaded was either not an image or a corrupted image.', form.errors['profile_image'][0])
