"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from journals.models import Entry, Journal, User, profile_image_upload_path
from unittest.mock import patch
import uuid
from django.utils import timezone
from datetime import timedelta

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'journals/tests/fixtures/default_user.json',
        'journals/tests/fixtures/other_users.json',
        'journals/tests/fixtures/default_template_owner.json',
        'journals/tests/fixtures/default_journals.json',
        'journals/tests/fixtures/default_entry.json'
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@johndoe'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_full_name_must_be_correct(self):
        full_name = self.user.full_name()
        self.assertEqual(full_name, "John Doe")

    def test_journals_recently_accessed_display_correct_values(self):
        before_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(before_result), 0)
        
        journal = Journal.objects.get(name='Default Journal')
        self.user.add_to_journals_recently_accessed(journal)
        after_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(after_result), 1)
        
        self.assertEqual(len(before_result) + 1, len(after_result))
        
    def test_journals_recently_accessed_cannot_hold_more_than_four_values(self):
        before_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(before_result), 0)
        
        journal = Journal.objects.get(name='Default Journal')
        self.user.add_to_journals_recently_accessed(journal)
        journal = Journal.objects.get(name='Second Journal')
        self.user.add_to_journals_recently_accessed(journal)
        after_result = self.user.get_recently_accessed_journals()
        self.assertEqual(after_result[0], journal)
        
        journal = Journal.objects.get(name='Third Journal')
        self.user.add_to_journals_recently_accessed(journal)
        after_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(after_result), 3)
        
        journal = Journal.objects.get(name='Fourth Journal')
        self.user.add_to_journals_recently_accessed(journal)
        after_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(after_result), 4)
        
        journal = Journal.objects.get(name='Fifth Journal')
        self.user.add_to_journals_recently_accessed(journal)
        after_result = self.user.get_recently_accessed_journals()
        self.assertEqual(len(after_result), 4)
        
        
        self.assertEqual(after_result[0], journal)
        self.assertEqual(after_result[1].name, "Fourth Journal")
        self.assertEqual(after_result[2].name, "Third Journal")
        self.assertEqual(after_result[3].name, "Second Journal")
    
    def test_get_journals_without_today_entry(self):
        journal_without_entry = self.user.get_journals_without_today_entry()
        #Should return all journals since none of them have any entries
        expected_result = Journal.objects.filter(owner=self.user)
        self.assertEqual(list(journal_without_entry), list(expected_result))
    
    def test_get_user_today_entries(self):
        journal_without_entry = self.user.get_user_today_entries()
        #Should return no entries
        self.assertEqual(list(journal_without_entry), [])
        
        journal = Journal.objects.get(name='Default Journal')
        entry = Entry.objects.create(
            journal=journal,
            entry_name = 'New Entry',
            responses = ['Response'],
            mood=None
        )
        
        journal_without_entry = self.user.get_user_today_entries()
        self.assertEqual(list(journal_without_entry), [entry])
    
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()


class ProfileImageUploadPathTest(TestCase):
    """Unit test for the profile_image_upload_path function."""

    def setUp(self):
        pass

    @patch('journals.models.uuid.uuid4')
    def test_profile_image_upload_path(self, mock_uuid):
        # Setup the return value for uuid4
        mock_uuid.return_value = uuid.UUID('12345678123456781234567812345678')
        
        # Call the function being tested
        upload_path = profile_image_upload_path(None, 'test_image.jpg')

        # Check that the filename was renamed properly with the mocked UUID
        expected_path = 'images/12345678123456781234567812345678.jpg'
        self.assertEqual(upload_path, expected_path)

class UserLoginTest(TestCase):
    """ Test last logged in feature for auto emails """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_user_never_logged_in(self):
        # User has never logged in
        self.user.last_login = None
        self.user.save()
        self.assertFalse(self.user.has_logged_in_last_24_hours())

    def test_user_logged_in_within_24_hours(self):
        # User logged in less than 24 hours ago
        self.user.last_login = timezone.now() - timedelta(hours=23)
        self.user.save()
        self.assertTrue(self.user.has_logged_in_last_24_hours())

    def test_user_logged_in_more_than_24_hours_ago(self):
        # User logged in more than 24 hours ago
        self.user.last_login = timezone.now() - timedelta(days=1, minutes=1)
        self.user.save()
        self.assertFalse(self.user.has_logged_in_last_24_hours())