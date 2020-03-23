# from django.test import TestCase, Client
# from django.urls import reverse
# from ..models import *
# import json
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.current_mumbers_url = reverse('current members')
#         self.login = reverse('login')
#         self.user = User.objects.create_user(username ="testuser", first_name="test", last_name="user", email="test@gmail.com", password="testpassword")
#         self.member = Member.objects.create(
#         user = self.user,
#         dateOfBirth="2020-01-01",
#         userType = "FamilyMember",
#         genderType = "Male",
#         )
#
#
#
#     def test_current_members_GET(self):
#         self.client.login(username=self.user.username)
#         self.client.post(self.login, {
#         'username' : 'testuser',
#         'password' : 'testpassword'
#         })
#         response = self.client.get(self.current_mumbers_url)
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(repsponse, 'mainapp/currentMembers.html')
