from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Notification


class NotificationsTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='notiuser1',
            password='Password123',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='notiuser2',
            password='Password123',
            email='user2@example.com'
        )
        self.notification = Notification.objects.create(
            user=self.user1,
            title='Weather Alert',
            message='Rain expected today.',
            notification_type='weather_alert',
            is_read=False
        )

    def test_list_notifications_unauthenticated(self):
        url = reverse('api:notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notifications_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Weather Alert')

    def test_user_cannot_access_other_user_notifications(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('api:notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_unread_count_action(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:notification-unread-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)

    def test_mark_read_action(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:notification-mark-read', kwargs={'pk': self.notification.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_read'], True)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_mark_all_read_action(self):
        # Create second unread notification
        Notification.objects.create(
            user=self.user1,
            title='Second Noti',
            message='Details',
            is_read=False
        )

        self.client.force_authenticate(user=self.user1)
        url = reverse('api:notification-mark-all-read')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)

        unread_count = Notification.objects.filter(user=self.user1, is_read=False).count()
        self.assertEqual(unread_count, 0)

    def test_generate_summary_action(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('api:notification-generate-summary')
        response = self.client.post(f"{url}?city=Madrid")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Madrid', response.data['title'])
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 2)
