"""Unit tests of the custom template creation form."""
from django.test import TestCase
from journals.forms import CustomTemplateForm
from journals.models import Template, User, Journal


class CustomTemplateTestCase(TestCase):
    """Unit tests of the Custom Template Creation form."""

    fixtures = [
        'journals/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(username='@johndoe')
        self.new_journal_name= 'Test Journal'
        self.form_input = {
            'journal_name': self.new_journal_name,
            'template_name': 'New Custom Template',
            'questions': "\nQuestion A \nQuestion B \nQuestion C \nQuestion D"
        }
        
    
    def test_valid_form_input(self):
        self._assert_form_is_valid()
    
    def test_custom_template_must_have_a_name(self):
        
        self.form_input['template_name'] = ''
        self._assert_form_is_invalid()
        
    def test_custom_template_must_have_an_owner(self):
        with self.assertRaises(Exception):
            form = CustomTemplateForm(owner=None, data=self.form_input)
            
    def test_custom_template_must_have_give_a_journal_name(self):
        self.form_input['journal_name'] = ''
        self._assert_form_is_invalid()

        
    def test_custom_template_must_have_questions(self):
        self.form_input['questions'] = ''
        self._assert_form_is_invalid()
    
    def test_form_converts_questions_field_into_list(self):
        form = CustomTemplateForm(owner=self.owner, data= self.form_input)
        expected_result = ['Question A', 'Question B', 'Question C', 'Question D']
        self.assertTrue(form.is_valid())
        cleaned_questions = form.cleaned_data.get('questions')
        self.assertEqual(cleaned_questions, expected_result)
    
    def test_form_converts_successfully_even_with_multiple_line_gaps(self):
        self.form_input['questions'] += '\n\n\nQuestion E'
        form = CustomTemplateForm(owner=self.owner, data= self.form_input)
        expected_result = ['Question A', 'Question B', 'Question C', 'Question D', 'Question E']
        self.assertTrue(form.is_valid())
        cleaned_questions = form.cleaned_data.get('questions')
        self.assertEqual(cleaned_questions, expected_result)
    
    def test_form_saves_correctly(self):
        before_template_count = Template.objects.filter(owner=self.owner).count()
        before_journal_count = Journal.objects.filter(owner=self.owner).count()
        form = CustomTemplateForm(owner=self.owner, data= self.form_input)
        new_journal = form.save()
        after_template_count = Template.objects.filter(owner=self.owner).count()
        after_journal_count = Journal.objects.filter(owner=self.owner).count()
        self.assertEqual(after_template_count, before_template_count + 1)
        self.assertEqual(form.cleaned_data.get('journal_name'), self.new_journal_name)
        self.assertEqual(after_journal_count, before_journal_count + 1)
        self.assertEqual(new_journal.name, self.new_journal_name)
        self.assertEqual(new_journal.owner, self.owner)
        new_template = new_journal.template
        
        expected_result = ['Question A', 'Question B', 'Question C', 'Question D']
        self.assertEqual(new_template.name, self.form_input['template_name'])
        self.assertEqual(new_template.get_questions(), expected_result)
        self.assertEqual(new_template.owner, self.owner)
    

        
    
    def _assert_form_is_valid(self):
        form = CustomTemplateForm(owner=self.owner, data= self.form_input)
        self.assertTrue(form.is_valid())
    
    def _assert_form_is_invalid(self):
        form = CustomTemplateForm(owner=self.owner, data= self.form_input)
        self.assertFalse(form.is_valid())