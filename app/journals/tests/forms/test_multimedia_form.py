from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from journals.forms import validate_multimedia_file_extension


class MultimediaFileExtensionValidatorTests(TestCase):
    def test_valid_file_extensions(self):
        valid_files = [
            SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
            SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mp3"),
            
        ]
        try:
            for file in valid_files:
                validate_multimedia_file_extension(file)
        except ValidationError:
            self.fail("validate_multimedia_file_extension raised ValidationError unexpectedly!")

    def test_invalid_file_extension(self):
        invalid_file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        with self.assertRaises(ValidationError):
            validate_multimedia_file_extension(invalid_file)