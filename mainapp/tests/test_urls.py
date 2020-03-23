from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *
from ..viewsCal import *

class TestUrls(SimpleTestCase):

    def test_index_url(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_todolists_url(self):
        url = reverse('todolists')
        self.assertEquals(resolve(url).func, todolist)

    def test_tasks_url(self):
        url = reverse('tasks', args=['1'])
        self.assertEquals(resolve(url).func, tasks)

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_current_members_url(self):
        url = reverse('current members')
        self.assertEquals(resolve(url).func, current_members)

    def test_lists_json_url(self):
        url = reverse('List of lists')
        self.assertEquals(resolve(url).func, lists_json)

    def test_create_list_url(self):
        url = reverse('create list')
        self.assertEquals(resolve(url).func, create_list)

    def test_complete_status_url(self):
        url = reverse('complete status')
        self.assertEquals(resolve(url).func, complete_status)

    def test_delete_list_url(self):
        url = reverse('delete list', args=['1'])
        self.assertEquals(resolve(url).func, delete_list)

    def test_delete_task_url(self):
        url = reverse('delete task')
        self.assertEquals(resolve(url).func, delete_task)

    def test_meal_planner_url(self):
        url = reverse('meal planner')
        self.assertEquals(resolve(url).func, meal_planner)

    def test_addmeal_url(self):
        url = reverse('add meal', args=['some-slug'])
        self.assertEquals(resolve(url).func, addmeal)

    def test_addmeal2_url(self):
        url = reverse('add meal 2')
        self.assertEquals(resolve(url).func, addmeal2)

    def test_deleteMeal_url(self):
        url = reverse('delete meal')
        self.assertEquals(resolve(url).func, deleteMeal)

    def test_addchore_url(self):
        url = reverse('add chore')
        self.assertEquals(resolve(url).func, addchore)

    def test_addreward_url(self):
        url = reverse('add reward')
        self.assertEquals(resolve(url).func, addreward)

    def test_claim_url(self):
        url = reverse('claim')
        self.assertEquals(resolve(url).func, claim)

    def test_delete_chore_url(self):
        url = reverse('delete chore')
        self.assertEquals(resolve(url).func, delete_chore)

    def test_delete_reward_url(self):
        url = reverse('delete reward')
        self.assertEquals(resolve(url).func, delete_reward)

    def test_chore_completed_url(self):
        url = reverse('chore completed')
        self.assertEquals(resolve(url).func, chore_completed)

    def test_chores_url(self):
        url = reverse('chores')
        self.assertEquals(resolve(url).func, chores)

    def test_accept_claim_url(self):
        url = reverse('accept claim')
        self.assertEquals(resolve(url).func, accept_claim)

    def test_choose_family_url(self):
        url = reverse('choose family')
        self.assertEquals(resolve(url).func, choose_family)

    def test_create_family_url(self):
        url = reverse('create family')
        self.assertEquals(resolve(url).func, create_family)

    def test_join_family_url(self):
        url = reverse('join family', args=['1'])
        self.assertEquals(resolve(url).func, join_family)

    def test_leave_family_url(self):
        url = reverse('leave family', args=['1'])
        self.assertEquals(resolve(url).func, leave_family)

    def test_search_key_url(self):
        url = reverse('search key')
        self.assertEquals(resolve(url).func, search_key)

    def test_share_key_url(self):
        url = reverse('share key')
        self.assertEquals(resolve(url).func, share_key)

    def test_chat_url(self):
        url = reverse('chat')
        self.assertEquals(resolve(url).func, chat)

    def test_add_message_json_url(self):
        url = reverse('add message')
        self.assertEquals(resolve(url).func, add_message)

    def test_location_url(self):
        url = reverse('location')
        self.assertEquals(resolve(url).func, location)

    def test_location_of_member_url(self):
        url = reverse('location of member')
        self.assertEquals(resolve(url).func, location_of_member)

    def test_get_credentials_url(self):
        url = reverse('calendar')
        self.assertEquals(resolve(url).func, get_credentials)

    def test_SignOutGoogle_url(self):
        url = reverse('SignOutGoogle')
        self.assertEquals(resolve(url).func, SignOutGoogle)

    def test_create_event_url(self):
        url = reverse('calendarAdd')
        self.assertEquals(resolve(url).func, create_event)
