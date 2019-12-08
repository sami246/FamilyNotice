from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from .enums import *

# Create your models here.
class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dateOfBirth = models.DateField(blank = False)
	userType = models.CharField(max_length = 50,
	 choices=userType.choices())
	profilePic = models.ImageField(upload_to = 'static/',
	 	default = 'static/empty-photo.jpg')

	def __str__(self):
		return self.user.username

class Task(models.Model):
	name = models.CharField(max_length=30)
	assignTo = models.ForeignKey(Member,
	 on_delete= models.CASCADE,
	 null=True, related_name='assign_to', blank=True)
	date = models.DateTimeField()
	description = models.TextField()
	completed = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class List(models.Model):
	nameOfList = models.CharField(max_length=30)
	task = models.ManyToManyField(Task)

	def __str__(self):
		# name = self.nameofFamily
		return self.nameOfList

# Create your models here.
class Family(models.Model):
	nameofFamily = models.CharField(max_length=30)
	members = models.ManyToManyField(Member)
	lists = models.ManyToManyField(List, blank=True)

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
	time = models.TimeField()
	location = models.CharField(max_length=30)

	def __str__(self):
		return self.title

class Chores(models.Model):
	name = models.CharField(max_length=30)
	reward = models.CharField(max_length=30)
	#May change to enum LATER and then even later add API
	description = models.TextField()
	dueBy = models.DateTimeField()
	assignTo = models.ForeignKey(Member, on_delete= models.CASCADE,
	 null=True, related_name='assign_to', blank=True)
	completed = models.BooleanField(default = False)


	def __str__(self):
		return self.name
