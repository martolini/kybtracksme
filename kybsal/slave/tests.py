from django.test import TestCase

from .models import Slave
from kybsal.timer.models import Action
from django.utils import timezone
class ActionTest(TestCase):

	def create_slave(self, username='test', password='test'):
		return Slave.objects.create(username=username, password=password)
	
	def create_action(self, slave, action="BREAK"):
		return Action.objects.create(action=action, slave=slave)

	def test_break_state(self):
		slave = self.create_slave()
		a = self.create_action(slave=slave)
		self.assertTrue(isinstance(a, Action))
		self.assertEqual(slave.get_current_state(), 2)

	def test_total_hours(self):
		slave=self.create_slave()
		a = self.create_action(slave=slave)
		self.assertTrue(isinstance(a,Action))
		self.assertEqual(slave.get_total_hours(slave.actions.all()), round((timezone.localtime(timezone.now())-a.started).seconds/3600.0,1))
	
	def test_session_state(self):
		slave = self.create_slave()
		a = self.create_action(action="SESSION", slave=slave)
		self.assertEqual(a.slave.get_current_state(), 1)

	def test_no_state(self):
		slave = self.create_slave()
		self.assertEqual(slave.get_current_state(), 0)

	def test_ineffective_hours(self):
		slave=self.create_slave()
		a = self.create_action(slave=slave)
		self.assertTrue(isinstance(a,Action))
		self.assertEqual(slave.get_ineffective_hours(slave.actions.all()), round((timezone.localtime(timezone.now())-a.started).seconds/3600.0,1))

	def test_effective_hours(self):
		slave=self.create_slave()
		a = self.create_action(slave=slave, action="SESSION")
		self.assertTrue(isinstance(a,Action))
		self.assertEqual(slave.get_effective_hours(slave.actions.all()), round((timezone.localtime(timezone.now())-a.started).seconds/3600.0,1))