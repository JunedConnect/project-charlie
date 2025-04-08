"""Unit tests for the Journal model."""
from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from journals.models import Entry, Journal, User
from django.utils import timezone
from datetime import timedelta


class JournalModelTestCase(TestCase):
    """Unit tests for the Journal model."""

    fixtures = [
        'journals/tests/fixtures/default_user.json',
        'journals/tests/fixtures/default_template_owner.json',
        'journals/tests/fixtures/default_journals.json',
        'journals/tests/fixtures/default_entry.json'
    ]


    def setUp(self):
        self.journal = Journal.objects.get(name='Default Journal')
    
    def test_journal_is_valid(self):
        self._assert_journal_is_valid()
    
    def test_journal_must_have_a_name(self):
        self.journal.name = ''
        self._assert_journal_is_invalid()
    
    def test_journal_name_can_be_50_characters(self):
        self.journal.name = 'a' * 50
        self._assert_journal_is_valid()
    
    def test_journal_name_cannot_be_more_than_50_characters_long(self):
        self.journal.name = 'a' * 51
        self._assert_journal_is_invalid()
        
    def test_journal_can_have_no_owner(self):
        self.journal.owner = None
        self._assert_journal_is_valid()
    
    def test_journal_must_have_a_template(self):
        self.journal.template = None
        self._assert_journal_is_invalid()
    
    def test_set_name_changes_the_journal_name(self):
        self.journal.set_name('TEST NAME')
        self.assertEqual(self.journal.name, 'TEST NAME')
    
    def test___str___returns_names(self):
        self.assertEqual(str(self.journal), self.journal.name)
    
    def test_get_entries(self):
        entries = list(self.journal.get_entries())
        expected_result = list(Entry.objects.filter(journal=self.journal))
        self.assertEqual(entries, expected_result)
    
    def test_check_if_today_entry_exists(self):
        self.assertFalse(self.journal.check_if_today_entry_exists())
        Entry.objects.create(journal=self.journal)
        self.assertTrue(self.journal.check_if_today_entry_exists())
        
    
    def test_get_date_of_journal_creation(self):
        expected_date = datetime(2024, 2, 22).date()
        date_of_creation = self.journal.get_date_of_journal_creation()
        self.assertEqual(date_of_creation, expected_date)
        
    def _assert_journal_is_valid(self):
        try:
            self.journal.full_clean()
        except (ValidationError):
            self.fail('Test journal should be valid')

    def _assert_journal_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.journal.full_clean()


class JournalModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='@john_doe', email='john@example.com', password='test12345')
        self.journal = Journal.objects.create(name="John's Journal", owner=self.user)

    def test_get_streak_with_no_entries(self):
        streak = self.journal.get_streak()
        self.assertEqual(streak, 0)

    def test_get_streak_with_break_in_streak(self):
        Entry.objects.create(journal=self.journal, date=timezone.now().date())
        Entry.objects.create(journal=self.journal, date=timezone.now().date() - timedelta(days=2))

        streak = self.journal.get_streak()
        self.assertEqual(streak, 1)

    def test_get_streak_with_resumed_streak(self):
        Entry.objects.create(journal=self.journal, date=timezone.now().date() - timedelta(days=2))
        streak = self.journal.get_streak()
        self.assertEqual(streak, 1)

    def tearDown(self):
        self.user.delete()
        self.journal.delete()
