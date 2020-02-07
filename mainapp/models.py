from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from .enums import *
from django.utils.crypto import get_random_string

# Create your models here.
class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dateOfBirth = models.DateField(blank = False)
	userType = models.CharField(max_length = 50,
	 choices=userType.choices())
	profilePic = models.ImageField(upload_to = 'static/',
	 	default = '/static/empty-photo.jpg')

	def __str__(self):
		return self.user.username

class Task(models.Model):
	name = models.CharField(max_length=30)
	assignTaskTo = models.ForeignKey(Member, on_delete= models.CASCADE, null=True, related_name='assign_task_to', blank=True)
	date = models.DateTimeField(blank=True, null=True)
	description = models.TextField(null=True, blank=True)
	completed = models.BooleanField(default = False)

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

	# def __str__(self):
	# 	return self.family.nameofFamily + " Meal Planner"

def create_new_ref_number():
      return get_random_string()

# Create your models here.
class Family(models.Model):
	nameofFamily = models.CharField(max_length=30)
	members = models.ManyToManyField(Member)
	lists = models.ManyToManyField(List, blank=True)
	mealPlan = models.OneToOneField(MealWeek, on_delete=models.CASCADE, blank=True, null=True)
	FamKey = models.CharField(max_length=30, default=create_new_ref_number, unique=True)

	def __str__(self):
		return self.nameofFamily

	# @property
	# def numberGroup(self):
	# 	return

class EventEntry(models.Model):
	title = models.CharField(max_length=30)
	membersInvolved = models.ManyToManyField(Member)
	description = models.TextField()
	date = models.DateField()
	location = models.CharField(max_length=30)
	start_time = models.TimeField()

	def __str__(self):
		return self.title

class Chores(models.Model):
	name = models.CharField(max_length=30)
	reward = models.CharField(max_length=30)
	#May change to enum LATER and then even later add API
	description = models.TextField()
	dueBy = models.DateTimeField()
	assignChoreTo = models.ForeignKey(Member, on_delete= models.CASCADE, null=True, related_name='assign_chore_to', blank=True)
	completed = models.BooleanField(default = False)


	def __str__(self):
		return self.name
