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
    plusone = models.BooleanField(default = False)

class ChoiceQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    vendors = models.ManyToManyField(Vendor,blank=True)
    finalized = models.BooleanField(default=False)

    def __unicode__(self):  
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)

class ChoiceResponse(models.Model):
    user_choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    username = models.CharField(max_length=50,blank=True)

    def __unicode__(self):  
        return self.user_choice.choice_text

class TextQuestion(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    vendors = models.ManyToManyField(Vendor,blank=True)
    finalized = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)


class TextResponse(models.Model):
    question = models.ForeignKey(TextQuestion,on_delete=models.CASCADE)
    response_text = models.CharField(max_length=100)
    username = models.CharField(max_length=50,blank=True)
    def __unicode__(self):
        return self.response_text