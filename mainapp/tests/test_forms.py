from django.test import TestCase
from ..forms import *

class TestForms(TestCase):

    def test_MealEntryForm_form_valid_data(self):
        form = MealEntryForm(data={
        'text' : "aovub",
        'description' : "pisancpn"
        })

        self.assertTrue(form.is_valid())

    def test_MealEntryForm_form_no_data(self):
        form = MealEntryForm(data={})
        self.assertFalse(form.is_valid())

    def test_RewardForm_form_valid_data(self):
        form = RewardForm(data={
        'name' : "aovub",
        'pointsNeeded' : "5"
        })

        self.assertTrue(form.is_valid())

    def test_RewardForm_form_no_data(self):
        form = RewardForm(data={})
        self.assertFalse(form.is_valid())

    def test_ChoreForm_form_valid_data(self):
        form = ChoreForm(data={
        'name' : "aovub",
        'points' : "5",
        'description' : 'apivb',
        'dueBy' : '2020-09-09 20:00:00'
        })

        self.assertTrue(form.is_valid())

    def test_ChoreForm_form_no_data(self):
        form = ChoreForm(data={})
        self.assertFalse(form.is_valid())

    def test_CalendarForm_form_valid_data(self):
        form = CalendarForm(data={
        'summary' : "aovub",
        'location' : "kx",
        'description' : 'apivb',
        'duration' : '3',
        'start_time' : 'feb 12th',
        })

        self.assertTrue(form.is_valid())

    def test_CalendarForm_form_no_data(self):
        form = CalendarForm(data={})
        self.assertFalse(form.is_valid())

    def test_CalendarForm_form_invalid_data(self):
        form = CalendarForm(data={
        'summary' : "aovub",
        'location' : "kx",
        'description' : 'apivb',
        'duration' : 'adba',
        'start_time' : 'feb 12th',
        })
        self.assertFalse(form.is_valid())

    def test_ListForm_form_valid_data(self):
        form = ListForm(data={
        'nameOfList' : "aovub",
        })

        self.assertTrue(form.is_valid())

    def test_ListForm_form_no_data(self):
        form = ListForm(data={})
        self.assertFalse(form.is_valid())

    def test_FamilyForm_form_valid_data(self):
        user1 = User.objects.create_user(username ="testuser", first_name="test", last_name="user", email="test@gmail.com", password="testpassword")
        member1 = Member.objects.create(
        user = user1,
        dateOfBirth="2020-01-01",
        userType = "FamilyMember",
        genderType = "Male",
        )
        Familyfff = Family.objects.create(nameofFamily="familyname")
        Familyfff.members.add(member1)
        Familyfff.save()
        filter = Member.objects.filter(family=Familyfff)
        form = FamilyForm(data={
        'nameofFamily' : "aovub",
        'members' : filter,
        })

        self.assertTrue(form.is_valid())

    def test_FamilyForm_form_no_data(self):
        form = FamilyForm(data={})
        self.assertFalse(form.is_valid())
