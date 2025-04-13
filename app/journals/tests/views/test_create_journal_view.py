"""Tests of the create journal view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from journals.forms import CreateNewJournal, CustomTemplateForm
from journals.models import Template, User
from journals.models import Journal
from journals.tests.helpers import reverse_with_next

class CreateJournalViewTestCase(TestCase):
    """Tests of the create journal view."""

    fixtures = ['journals/tests/fixtures/default_user.json',
                'journals/tests/fixtures/default_template_owner.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.template = Template.objects.get(name='Base Template')
        self.url = reverse('create_journal')
        self.form_input = {
            'journal_name': 'testing123',
            'template': self.template.id,
        }

    def test_create_journal_url(self):
        self.assertEqual(self.url,'/journals/create_journal/')

    def test_get_create_journal(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_journal.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateNewJournal))
        self.assertFalse(form.is_bound)

    def test_get_create_journal_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccessful_create_journal(self):
        before_count = Journal.objects.count()
        self.form_input['journal_name'] = "a" * 51 #max length is 50 characters 
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Journal.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('journals_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'journals_base.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_succesful_create_journal(self):
        before_count = Journal.objects.count()
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Journal.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('journals_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'journals_base.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        journal = Journal.objects.get(name='testing123')
        self.assertTrue(self.user == journal.owner)
        self.assertEqual(journal.owner,self.user)

    def test_selecting_custom_template_redirects_to_custom_template_view(self):
        template = Template.objects.get(name='Custom Template')
        self.form_input['template'] = template.id
        before_count = Journal.objects.count()
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Journal.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('custom_template')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'custom_template.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CustomTemplateForm))
        self.assertContains(response, f'<input type="text" name="journal_name" value="{self.form_input["journal_name"]}"')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
