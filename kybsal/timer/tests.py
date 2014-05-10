from django.test import TestCase
from kybsal.slave.models import Slave
from django.core.urlresolvers import reverse
from django.test.client import Client
from .models import Action


class TimerTest(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = Slave.objects.create_user('test', 'test@test.com', 'test')

	def create_slave(self, username='test', password='test'):
		return Slave.objects.create(username=username, password=password)

	def test_sjekk_inn(self):
		self.client.login(username='test', password='test')
		response = self.client.get(reverse('sjekk_in'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.user.get_current_state(), 1)

	def test_logout(self):
		self.test_sjekk_inn()
		self.assertEqual(self.user.get_current_state(), 1)
		response = self.client.get(reverse('logout'), follow=True)
		self.assertEqual(self.user.get_current_state(), 0)

	def test_break(self):
		self.test_sjekk_inn()
		response = self.client.get(reverse('pause'))
		self.assertEqual(self.user.get_current_state(), 2)
		self.assertTrue(self.user.get_current_action().is_break())
		response = self.client.get(reverse('pause'))
		self.assertEqual(self.user.get_current_state(), 1)
		self.assertTrue(self.user.get_current_action().is_session())

	def test_whole_loop(self):
		self.test_break()
		self.test_logout()
		self.assertEqual(self.user.get_current_action(), None)
		self.assertEqual(self.user.get_current_state(), 0)

	def test_mange_sjekkins(self):
		self.test_sjekk_inn()
		self.test_sjekk_inn()
		self.test_sjekk_inn()
		self.assertEqual(self.user.get_current_state(), 1)
		self.assertTrue(self.user.get_current_action().is_session())
		self.assertEqual(self.user.feed.count(), 1)
