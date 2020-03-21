from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from .enums import *
import json
from django.core.serializers import serialize

import google.oauth2.credentials
from google.auth import credentials

# Create your models here.
class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dateOfBirth = models.DateField(blank = False)
	userType = models.CharField(max_length = 50,
	 choices=userType.choices())
	genderType = models.CharField(max_length = 50,
	 choices=genderType.choices(), null=True)
	profilePic = models.ImageField(upload_to = 'static/',
	 	default = 'static/empty-photo.jpg')
	points = models.PositiveIntegerField(default="0")
	Currentpoints = models.PositiveIntegerField(default="0")
	# tasksCompleted = models.PositiveIntegerField(default="0")
	# cred = google.oauth2.credentials.Credentials('access_token')
	long = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
	lat = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
	timeOfLocation = models.CharField(max_length = 50,null=True, blank=True)

	def __str__(self):
		str = self.user.username + " : " + self.user.first_name + " " + self.user.last_name
		return self.user.username

	@property
	def Level(self):
		point = self.points
		return "Level " + str((point//10)+1)

	@property
	def NumbOfFamilies(self):
		families = Family.objects.filter(members=self.id)
		# ListOfFamilies = ', '.join(str(e) for e in families)
		# return "Families : " + str(ListOfFamilies)
		return len(families)

	@property
	def MessagesSent(self):
		messages = Message.objects.filter(author=self.id)
		return len(messages)

	@property
	def TasksComp(self):
		tasks = Task.objects.filter(assignTaskTo=self.id).filter(completed=True)
		chores = Chores.objects.filter(assignChoreTo=self.id).filter(completed=True)
		num = len(tasks) + len(chores)
		return num

	@property
	def Tasks(self):
		tasks = Task.objects.filter(assignTaskTo=self.id)
		permission_serialize= json.loads(serialize('json', tasks))
		return permission_serialize

class Task(models.Model):
	name = models.CharField(max_length=30)
	assignTaskTo = models.ForeignKey(Member, on_delete= models.CASCADE, null=True, related_name='assign_task_to', blank=True)
	date = models.DateTimeField(blank=True, null=True)
	description = models.TextField(null=True, blank=True)
	completed = models.BooleanField(default = False)
	chore = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class List(models.Model):
	nameOfList = models.CharField(max_length=30)
	task = models.ManyToManyField(Task, blank=True)

	@property
	def taskCompleted(self):
		o = List.objects.get(pk = self.id)
		for group in o.task.all():
			if group.completed==False:
				return False
		return True



	def __str__(self):
		# name = self.nameofFamily
		return self.nameOfList

class MealDesc(models.Model):
	text = models.CharField(default=None, max_length=30, null=True, unique=False)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.text

# class Meal(models.Model):
# 	mealType = models.CharField(max_length = 50,
# 	 choices= DaysMeals.choices(), unique=True)
# 	meal = models.CharField(max_length=30)
# 	description = models.TextField(blank = True)
#
#
# 	def __str__(self):
# 		return self.meal + " " + self.mealType

class MealWeek(models.Model):
	monB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="monb", null=True, default=None, unique=False, blank=True)
	monL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="monL", null=True, default=None, unique=False, blank=True)
	monD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="monD", null=True, default=None, unique=False, blank=True)
	tueB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="tueB", null=True, default=None, unique=False, blank=True)
	tueL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="tueL", null=True, default=None, unique=False, blank=True)
	tueD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="tueD", null=True, default=None, unique=False, blank=True)
	wedB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="wedB", null=True, default=None, unique=False, blank=True)
	wedL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="wedL", null=True, default=None, unique=False, blank=True)
	wedD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="wedD", null=True, default=None, unique=False, blank=True)
	thuB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="thuB", null=True, default=None, unique=False, blank=True)
	thuL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="thuL", null=True, default=None, unique=False, blank=True)
	thuD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="thuD", null=True, default=None, unique=False, blank=True)
	friB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="friB", null=True, default=None, unique=False, blank=True)
	friL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="friL", null=True, default=None, unique=False, blank=True)
	friD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="friD", null=True, default=None, unique=False, blank=True)
	satB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="satB", null=True, default=None, unique=False, blank=True)
	satL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="satL", null=True, default=None, unique=False, blank=True)
	satD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="satD", null=True, default=None, unique=False, blank=True)
	sunB = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="sunB", null=True, default=None, unique=False, blank=True)
	sunL = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="sunL", null=True, default=None, unique=False, blank=True)
	sunD = models.OneToOneField(MealDesc, on_delete=models.SET_NULL, related_name="sunD", null=True, default=None, unique=False, blank=True)

	def __str__(self):
		string = str(self.family) + " Meal Planner"
		return string

from django.utils.crypto import get_random_string
def create_new_ref_number():
      return get_random_string()


class Message(models.Model):
	author = models.ForeignKey(Member, on_delete= models.PROTECT, related_name='author')
	message = models.CharField(max_length=200)
	timePublished = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to = 'static/', null=True, blank=True)

	def __str__(self):
		return self.message

	@property
	def dateFormatted(self):
		myDate = self.timePublished
		print('My Date: ', myDate)
		formatedDate = myDate.strftime("%H:%M %m/%d")
		print('formated Date: ', formatedDate)
		return formatedDate

class Chatroom(models.Model):
	name = models.CharField(max_length=30, default="Family Chatroom")
	messages = models.ManyToManyField(Message, blank=True)

	def __str__(self):
		string = str(self.family) + " Chatroom"
		return string

class EventEntry(models.Model):
	summary = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	location = models.CharField(max_length=30, blank=True, null=True)
	start_time = models.CharField(max_length=50)
	duration = models.PositiveIntegerField(default="1")

	def __str__(self):
		return self.summary

class Rewards(models.Model):
	name = models.CharField(max_length=30)
	pointsNeeded = models.PositiveIntegerField()

	def __str__(self):
		return self.name

class ClaimReward(models.Model):
	name = models.CharField(max_length=30)
	member = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Chores(models.Model):
	name = models.CharField(max_length=30)
	points = models.PositiveIntegerField()
	#May change to enum LATER and then even later add API
	description = models.TextField(null=True, blank=True)
	dueBy = models.DateTimeField(null=True, blank=True)
	assignChoreTo = models.ManyToManyField(Member, blank=True)
	completed = models.BooleanField(default = False)

	def __str__(self):
		return self.name

	@property
	def dateFormatted(self):
		try:
			myDate = self.dueBy
			print('My Date: ', myDate)
			formatedDate = myDate.strftime("%H:%M | %a %d/%m")
			print('formated Date: ', formatedDate)
		except:
			formatedDate = ""
		return formatedDate

	@property
	def nameofAssigned(self):
		members = Member.objects.filter(chores=self.id)
		arr = []
		names = [ mem.user.first_name for mem in members ]
		return names


class ChoreList(models.Model):
	chores = models.ManyToManyField(Chores, blank=True)
	rewards = models.ManyToManyField(Rewards, blank=True)
	claim = models.ManyToManyField(ClaimReward, blank=True)

	def __str__(self):
		string = str(self.family) + " Chore List"
		return string

# Create your models here.
class Family(models.Model):
	nameofFamily = models.CharField(max_length=30)
	members = models.ManyToManyField(Member)
	lists = models.ManyToManyField(List, blank=True)
	mealPlan = models.OneToOneField(MealWeek, on_delete=models.CASCADE, null=True)
	chatroom = models.OneToOneField(Chatroom, on_delete=models.CASCADE, null=True)
	FamKey = models.CharField(max_length=30, default=create_new_ref_number, unique=True)
	cal = models.BooleanField(default=False)
	calId = models.CharField(max_length=60, null=True, blank=True)
	calEvents = models.ManyToManyField(EventEntry, blank=True)
	choreList = models.OneToOneField(ChoreList, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.nameofFamily

	@property
	def nameOfFamilyMembers(self):
		members = Member.objects.filter(family=self.id)
		arr = []
		names = [ [mem.user.first_name, mem.id] for mem in members ]
		return names

	@property
	def idOfFamilyMembers(self):
		members = Member.objects.filter(family=self.id)
		arr = []
		names = [ mem.id for mem in members ]
		return names
