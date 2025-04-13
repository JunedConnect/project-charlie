from django.test import TestCase
from django.urls import reverse
from journals.models import User
from django.conf import settings

class DashboardViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'Password123'
        for i in range(12):
            email = f'user{i}@example.com' 
            user = User.objects.create_user(username=f'user{i}', email=email, password=cls.password)
            profile = user.profile
            profile.level = 12 - i
            profile.experience = (12 - i) * 100
            profile.save()

        # Set the test subject
        cls.user = User.objects.get(username='user11')
        cls.url = reverse('dashboard')

    def setUp(self):
        self.client.login(username=self.user.username, password=self.password)


    def test_log_in_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_dashboard_view_with_leaderboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('top_users', response.context)
        self.assertTrue(len(response.context['top_users']) <= 10)
        self.assertEqual(response.context['top_users'][0].user.username, 'user0')
        
    def test_user_rank_displayed_correctly_for_user_outside_top_10(self):
        response = self.client.get(self.url)
        self.assertIn('current_user_rank', response.context)
        self.assertTrue(response.context['current_user_rank'] > 10)

    def test_dashboard_view_redirect_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('log_in')}?next={self.url}")

    def test_leaderboard_content_for_top_10_users(self):
        response = self.client.get(self.url)
        for i, profile in enumerate(response.context['top_users'], start=1):
            self.assertContains(response, profile.user.username)
            self.assertContains(response, profile.level)
            if profile.achievements.exists():
                self.assertContains(response, profile.achievements.first().name)

    def test_current_user_rank_and_details_in_leaderboard(self):
        self.client.login(username='user11', password=self.password)
        response = self.client.get(self.url)
        self.assertIn('current_user_rank', response.context)
        self.assertContains(response, 'user11')  
        self.assertContains(response, response.context['current_user_rank'])  