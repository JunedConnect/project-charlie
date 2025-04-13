"""Unit tests of the custom template creation form."""
from django import forms
from django.test import TestCase
from journals.forms import CustomTemplateForm, SearchForm
from journals.models import Entry, Template, User, Journal


class SearchFormTestCase(TestCase):
    """Unit tests of the Search form."""

    """
    Of all the fixtures in this list, only objects from the 'default_{file}.json' are being used
    The others are required simply so that only 1 possible value would be in the queryset
    for the search entry test
    """
    fixtures = [
        'journals/tests/fixtures/default_user.json',
        'journals/tests/fixtures/default_template_owner.json',
        'journals/tests/fixtures/default_journals.json',
        'journals/tests/fixtures/default_entry.json',
        'journals/tests/fixtures/other_users.json',
        'journals/tests/fixtures/other_journal.json',
        'journals/tests/fixtures/other_entry.json',
    ]

    def setUp(self):
        self.owner = User.objects.get(username='@johndoe')
        self.journal_with_entry = Journal.objects.filter(owner=self.owner).get(name="Default Journal")
        
    
        self.form_input = {
            'search_name': 'irst'
        }
        
        self.model = Entry
        self.model_name_field = 'entry_name'
        self.foreign_key = 'journal'
        self.foreign_key_value = self.journal_with_entry
        

    def test_search_filter_returns_correct_output(self):
        """Test queryset only has 1 value (from journal.id 1) in it """       
        search_result = self._get_filtered_results_from_search_form()
        entry_from_search_result = search_result.get(entry_name="First entry")
        target_entry = Entry.objects.filter(journal=self.journal_with_entry).get(entry_name="First entry") 
        
        self.assertEqual(search_result.count(), 1)
        self.assertEqual(entry_from_search_result, target_entry)
        self.assertEqual(entry_from_search_result.journal.id, 1)
        self.assertEqual(entry_from_search_result.id, 1)
        

    def test_search_filter_accepts_blank_search_name(self):
        self.form_input['search_name'] = '' 
        search_result = self._get_filtered_results_from_search_form()
        expected_result = Entry.objects.filter(journal=self.journal_with_entry)
        self.assertEqual(search_result.count(), 2)
        self.assertEqual(list(search_result), list(expected_result))
        
        

        
    def test_search_filter_works_with_other_models(self):
        self.model = Journal
        self.model_name_field = 'name'
        self.foreign_key = 'owner'
        self.foreign_key_value = self.owner
        
        self.form_input['search_name'] = 'Default'
        search_results = self._get_filtered_results_from_search_form()
        self.assertEqual(search_results.count(), 1)
        journal_from_search_result = search_results.get(name="Default Journal")
        self.assertEqual(journal_from_search_result, self.journal_with_entry)
        
        self.assertEqual(journal_from_search_result.owner, self.owner)
        
    def test_search_filter_works_with_models_that_dont_use_a_foreign_key(self):
        self.model = User
        self.model_name_field = "username"
        self.form_input['search_name'] = 'doe'
        form = SearchForm(model=self.model, model_name_field=self.model_name_field, data=self.form_input)
        search_result = form.get_filtered_results()
        expected_result = User.objects.filter(username__icontains="doe")
        
        self.assertEqual(search_result.count(), 2)
        self.assertEqual(list(search_result), list(expected_result))
        
        
        
        """
        Create test for the search form
        Use entry as the main search but also do a test for searching journals
        test that the same works with journals as well but only need to test that you can use a different model and the code still works

        """
        
    def test_model_must_be_provied(self):
        self.model = None
        with self.assertRaises(ValueError):        
            form = SearchForm(model=self.model, 
                            model_name_field=self.model_name_field, 
                            model_foreign_key= self.foreign_key, 
                            model_foreign_key_value= self.foreign_key_value, 
                            data=self.form_input)
    
    def test_model_name_field_must_be_provied(self):
        self.model_name_field = None
        with self.assertRaises(ValueError):        
            form = SearchForm(model=self.model, 
                            model_name_field=self.model_name_field, 
                            model_foreign_key= self.foreign_key, 
                            model_foreign_key_value= self.foreign_key_value, 
                            data=self.form_input)
            
    def test_model_attribute_must_be_subclass_of_Model(self):
        self.model = SearchForm
        with self.assertRaises(ValueError):        
            form = SearchForm(model=self.model, 
                            model_name_field=self.model_name_field, 
                            model_foreign_key= self.foreign_key, 
                            model_foreign_key_value= self.foreign_key_value, 
                            data=self.form_input)
        
    def _get_filtered_results_from_search_form(self):
        form = SearchForm(model=self.model, 
                          model_name_field=self.model_name_field, 
                          model_foreign_key= self.foreign_key, 
                          model_foreign_key_value= self.foreign_key_value, 
                          data=self.form_input)
        
        return form.get_filtered_results()

        
            