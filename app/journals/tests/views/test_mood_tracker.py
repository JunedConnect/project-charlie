from django.test import TestCase
from journals.forms import MoodTrackerForm
from django.contrib import messages
from django.test import TestCase

class MoodTrackerFormTest(TestCase):
    def test_mood_choices(self):
        form = MoodTrackerForm()
        
        # Check if the mood field has the correct choices
        self.assertEqual(form.fields['mood'].choices, [
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('neutral', 'Neutral'),
            ('angry', 'Angry'),
        ])
    
    def test_valid_form(self):
        # Test data for a valid form submission
        valid_data = {'mood': 'happy'}
        
        form = MoodTrackerForm(data=valid_data)
        
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        # Test data for an invalid form submission
        invalid_data = {'mood': ''}
        
        form = MoodTrackerForm(data=invalid_data)
        
        self.assertFalse(form.is_valid())
        # Check if the correct error message is displayed
        self.assertEqual(form.errors['mood'], ['This field is required.'])