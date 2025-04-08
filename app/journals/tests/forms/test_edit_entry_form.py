from django.test import TestCase
from django import forms
from journals.models import User, Template, Journal, Entry
from journals.forms import EditEntryForm, MoodTrackerForm, validate_multimedia_file_extension

class EditEntryFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='@testuser', email='test@example.com', password='testpassword')
        cls.template = Template.objects.create(name="Test Template", owner=cls.user, questions=["Q1", "Q2"])
        cls.journal = Journal.objects.create(name="Test Journal", owner=cls.user, template=cls.template)
        cls.entry = Entry.objects.create(journal=cls.journal, entry_name="Test Entry", responses=["A1", "A2"])

    def test_form_with_valid_data(self):
        
        form_data = {
            'entry_name': 'Updated Entry Name',
            'mood': 'happy',
            'question_0': 'Answer 1',
            'question_1': 'Answer 2',
        }
        form = EditEntryForm(data=form_data, instance=self.entry, questions=self.template.questions)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_saves_properly(self):
        form_data = {
            'entry_name': 'Another Entry Name',
            'question_0': 'New Answer 1',
            'question_1': 'New Answer 2',
        }
        mood_form_data = {'mood': 'neutral'}
        form = EditEntryForm(data=form_data, instance=self.entry, questions=self.template.questions)
        mood_form = MoodTrackerForm(data=mood_form_data)
        if form.is_valid() and mood_form.is_valid():
            entry = form.save(commit=False)
            entry.mood = mood_form.cleaned_data['mood']
            entry.save()
            self.assertEqual(entry.entry_name, form_data['entry_name'])
            self.assertEqual(entry.mood, mood_form_data['mood'])
            self.assertEqual(len(entry.responses), 2, "The number of responses should be exactly 2")


class EditEntryFormInitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='@testuser', password='password', email='test@example.com')
        self.template = Template.objects.create(name="Test Template", owner=self.user, questions=["What did you learn today?", "How do you feel?"])
        self.journal = Journal.objects.create(name="Test Journal", owner=self.user, template=self.template)
        self.entry = Entry.objects.create(journal=self.journal, entry_name="Test Entry")

    def test_form_initialization_with_questions(self):
        questions = ["What did you learn today?", "How do you feel?"]
        form = EditEntryForm(instance=self.entry, questions=questions)

        self.assertIsInstance(form.fields['mood'], forms.ChoiceField, "Mood field is not initialized correctly")
        self.assertTrue(any(isinstance(validator, type(validate_multimedia_file_extension)) for validator in form.fields['multimedia_file'].validators), "Multimedia file validators are not correctly appended")

        for i, question in enumerate(questions):
            field_name = f'question_{i}'
            self.assertIn(field_name, form.fields, f"Field '{field_name}' not in form fields")
            self.assertIsInstance(form.fields[field_name], forms.CharField, f"Field '{field_name}' is not a CharField")
            self.assertEqual(form.fields[field_name].label, question, f"Field '{field_name}' does not have the correct label")

    def test_form_initialization_with_responses(self):
        questions = ["What did you learn today?", "How do you feel?"]
        responses = ["Django testing", "Happy"]
        self.entry.responses = responses
        self.entry.save()

        form = EditEntryForm(instance=self.entry, questions=questions)
        
        for i, expected_response in enumerate(responses):
            actual_response = form.initial_responses(i)
            self.assertEqual(actual_response, expected_response, f"Initial response for question {i} does not match expected value.")