from django.db import models
from django.shortcuts import render

# Create your models here.
class Pages(models.Model):
	url = models.CharField(max_length=255)	
	parsed_text = models.TextField()
	is_indexed = models.BooleanField()


class Indexes(models.Model):
	word = models.CharField(max_length=100)
	url = models.CharField(max_length=255)	
	
