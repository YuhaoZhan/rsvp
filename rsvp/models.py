from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):  
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):  
        return self.name   

class Owner(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Vendor(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Guest(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)

class Event(models.Model):
    name = models.CharField(max_length=30)
    time = models.DateTimeField('Date Post')
    owners = models.ManyToManyField(Owner, blank=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    guests = models.ManyToManyField(Guest, blank=True)

class ChoiceQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    visible = models.BooleanField(default=True)

class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)

class ChoiceResponse(models.Model):
    user_choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    username = models.CharField(max_length=50,blank=True)

class TextQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    visible = models.BooleanField(default=True)

class TextResponse(models.Model):
    question = models.ForeignKey(TextQuestion,on_delete=models.CASCADE)
    response_text = models.CharField(max_length=100)
    username = models.CharField(max_length=50,blank=True)