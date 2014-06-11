from django.test import *
from django.core.urlresolvers import reverse
from demo.models import *
import unittest

from django.test.client import Client
from allauth.account.models import EmailAddress, EmailConfirmation

class ProjectTestCases(TestCase):
	def setUp(self):
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		Project.newProject("Test description", "Test Solution", "Test Industry", "Test Video", "Project1", user)
		User.objects.create_user('timmy', 'timmy@eng.com', 'timmypassword')

	def test_new_profile(self):
		user = User.objects.get(email='lennon@thebeatles.com')
		profile = user.profile
		self.assertEqual(profile.user_id, user.id)
	
	def test_new_project(self):
		user = User.objects.get(email='lennon@thebeatles.com')
		created = Project.newProject("Test description", "Test Solution", "Test Industry", "Test Video", "Project2", user)
		self.assertEqual(created, True)
		
		project = Project.objects.get(title="Project2")
		team = Project.getTeamMembers(project)
		self.assertIn(user, team)
		
	def test_add_person(self):
		user = User.objects.get(email='timmy@eng.com')
		project = Project.objects.get(title="Project1")
		team = Project.getTeamMembers(project)	
		self.assertNotIn(user, team)
		
		Project.addMember(project.title, user.email)
		team = Project.getTeamMembers(project)
		self.assertIn(user, team)
		
class URLTestCases(TestCase):
	
	user = None

	def setUp(self):
		user = User.objects.create(username='timmy')
		user.set_password('timmypassword')
		user.save()
		EmailAddress.objects.create(user=user,
									email='timmy@timmtwebsite.com',
									primary=True,
									verified=True)

	def test_view_pages_not_logged_in(self):
		response = self.client.get('/demo/dashboard', follow=True)
		self.assertTemplateNotUsed('demo/loggedindefault.html')
		
		
	def test_call_view_denies_anonymous(self):
		response = self.client.get(reverse('dashboard'), follow=True)
		self.assertTemplateNotUsed('demo/loggedindefault.html')
		response = self.client.post(reverse('dashboard'), follow=True)
		self.assertTemplateNotUsed('demo/loggedindefault.html')

	def test_call_view_loads(self):
		self.client.login(username='timmy', password='timmypassword')  # defined in fixture or with factory in setUp()
		response = self.client.get('/demo/dashboard')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'demo/loggedindefault.html')

