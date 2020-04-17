from django.db import models
from django.contrib.auth.models import AbstractUser
from lms_api.enums import UserGender
from django.db.models import CharField, PositiveSmallIntegerField, TextField, ForeignKey, ManyToManyField, Model
# Create your models here.
class User(AbstractUser):
	phone_no = CharField(max_length=20)
	gender = PositiveSmallIntegerField(default=UserGender.UNKNOWN, choices=UserGender.CHOICES)

	class Meta(AbstractUser.Meta):
		abstract = False

	def __str__(self):
		return self.username

class Category(Model):
	name = CharField(max_length=30)
	def __str__(self):
		return self.name

class Publisher(Model):
	name = CharField(max_length=256)
	def __str__(self):
		return self.name

class Author(Model):
	name = CharField(max_length=256)
	def __str__(self):
		return self.name

class Book(Model):
	title = CharField(max_length=256)
	desc = TextField()
	publisher = ForeignKey(Publisher,related_name="books", on_delete=models.CASCADE)
	author = ForeignKey(Author,related_name="books", on_delete=models.CASCADE)
	categories = ManyToManyField(Category,related_name="books")
	def __str__(self):
		return self.title
