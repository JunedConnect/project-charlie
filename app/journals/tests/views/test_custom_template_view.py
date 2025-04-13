"""Tests of the create journal view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from journals.forms import CustomTemplateForm
from journals.models import Template, User
from journals.models import Journal
from journals.tests.helpers import reverse_with_next


class CreateJournalViewTestCase(TestCase):
    """Tests of the create journal view."""

    fixtures = ['journals/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.new_journal_name = 'Test Journal'
        self.url = reverse('custom_template')
        self.form_input = {
            'journal_name': self.new_journal_name,
            'template_name': 'New template',
            'questions': 'Question A \nQuestion B \nQuestion C \n\n\nQuestion D',
            
        }

    def test_custom_template_url(self):
        expected_url = "/custom_template/"
        self.assertEqual(self.url, expected_url)

    def test_get_custom_template(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_template.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CustomTemplateForm))
        self.assertFalse(form.is_bound)

    def test_get_custom_template_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)       
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_unsuccessful_custom_template(self):

        before_template_count = Template.objects.count()
        before_journal_count = Journal.objects.count()
        
        self.form_input['questions'] = "" 
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_journal_count = Journal.objects.count()
        after_template_count = Template.objects.count()
        self.assertEqual(after_journal_count, before_journal_count)
        self.assertEqual(after_template_count, before_template_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_template.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CustomTemplateForm))
        self.assertTrue(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)  

    def test_succesful_custom_template(self):
        before_template_count = Template.objects.count()
        before_journal_count = Journal.objects.count()

        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_journal_count = Journal.objects.count()
        after_template_count = Template.objects.count()
        self.assertEqual(after_journal_count, before_journal_count + 1)
        self.assertEqual(after_template_count, before_template_count + 1)
        response_url = reverse('journals_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'journals_base.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        new_template = Template.objects.get(name=self.form_input['template_name'])
        expected_questions = ['Question A', 'Question B', 'Question C', 'Question D']
        self.assertTrue(self.user == new_template.owner)
        self.assertEqual(new_template.get_questions(), expected_questions)
        new_journal = Journal.objects.get(name=self.form_input['journal_name'])
        self.assertEqual(new_journal.owner, self.user)
        self.assertEqual(new_journal.template, new_template)
        journal_name_from_session_data = self.client.session.get('journal_name', None)
        self.assertEqual(journal_name_from_session_data, None)
    


    def test_succesful_custom_template_using_session_data(self):
        different_journal_name = 'OTHER JOURNAL'
        session_data = {'journal_name': different_journal_name}
        session = self.client.session
        session.update(session_data)
        session.save()
        del self.form_input['journal_name']
        before_template_count = Template.objects.count()
        before_journal_count = Journal.objects.count()

        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_journal_count = Journal.objects.count()
        after_template_count = Template.objects.count()
        self.assertEqual(after_journal_count, before_journal_count + 1)
        self.assertEqual(after_template_count, before_template_count + 1)
        response_url = reverse('journals_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'journals_base.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        new_template = Template.objects.get(name=self.form_input['template_name'])
        expected_questions = ['Question A', 'Question B', 'Question C', 'Question D']
        self.assertTrue(self.user == new_template.owner)
        self.assertEqual(new_template.get_questions(), expected_questions)
        new_journal = Journal.objects.get(name=different_journal_name)
        self.assertEqual(new_journal.owner, self.user)
        self.assertEqual(new_journal.template, new_template)
        journal_name_from_session_data = self.client.session.get('journal_name', None)
        self.assertEqual(journal_name_from_session_data, None)
        