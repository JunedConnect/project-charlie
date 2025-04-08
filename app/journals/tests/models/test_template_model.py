"""Unit tests for the template model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from journals.models import Template

class templateModelTestCase(TestCase):
    """Unit tests for the Template model."""

    fixtures = [
        'journals/tests/fixtures/default_template_owner.json',
    ]


    def setUp(self):
        self.template = Template.objects.get(name='Base Template')
    
    def test_template_is_valid(self):
        self._assert_template_is_valid()
        
    def test_template_must_have_a_name(self):
        self.template.name = ''
        self._assert_template_is_invalid()
    
    def test_template_name_can_be_50_characters(self):
        self.template.name = 'a' * 50
        self._assert_template_is_valid()
    
    def test_template_name_cannot_be_more_than_50_characters_long(self):
        self.template.name = 'a' * 51
        self._assert_template_is_invalid()
        
    def test_template_can_have_no_owner(self):
        self.template.owner = None
        self._assert_template_is_valid()
    
    def test_template_must_have_questions(self):
        self.template.questions = []
        self._assert_template_is_invalid()
        
    def test_get_questions(self):
        questions = list(self.template.get_questions())
        expected = self.template.questions
        self.assertEqual(questions, expected)
    
    def test_set_questions(self):
        new_questions = ['A', 'B', 'C']
        self.template.set_questions(new_questions)
        self.assertEqual(self.template.questions, new_questions)
        
    def test___str__(self):
        self.assertEqual(str(self.template), self.template.name)
    
    def test_add_question(self):
        questions_before = self.template.get_questions()
        new_question = 'My question'
        questions_before.append(new_question)
        self.template.add_question(new_question)
        self.assertEqual(self.template.get_questions(), questions_before)
        
    def test_add_question_with_empty_question(self):
        questions_before = self.template.get_questions()
        new_question = None
        self.template.add_question(new_question)
        self.assertEqual(self.template.get_questions(), questions_before)
        
                
    def _assert_template_is_valid(self):
        try:
            self.template.full_clean()
        except (ValidationError):
            self.fail('Test template should be valid')

    def _assert_template_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.template.full_clean()
            