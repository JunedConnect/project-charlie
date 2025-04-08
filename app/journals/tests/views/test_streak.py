from datetime import datetime, timedelta

from django.test import TestCase
from journals.models import User, Journal, Entry

class JournalTestCase(TestCase):
    """Test case for the Journal model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password="Password123"
        )

        self.journal = Journal.objects.create(name='Test Journal', owner=self.user)

    def test_get_streak(self):

        current_date = datetime.now()

        Entry.objects.create(journal=self.journal, date=current_date)
        Entry.objects.create(journal=self.journal, date=current_date - timedelta(days=1))
        Entry.objects.create(journal=self.journal, date=current_date - timedelta(days=2))

        self.assertEqual(self.journal.get_streak(), 1)

    def test_get_streak_gap(self):
        

        
        Entry.objects.create(journal=self.journal, date=datetime.now() - timedelta(days=0))
        Entry.objects.create(journal=self.journal, date=datetime.now() - timedelta(days=2))

        self.assertEqual(self.journal.get_streak(), 1)