# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def validate(self, request):
        errors = False
        ###########################################################
        # validations here
        if len(request.POST['fname']) < 2:
            messages.error(request,'First name must be at least 2 characters!')
            errors = True  
        if not request.POST['fname'].isalpha():
            messages.error(request,"First name should be alpha only")
            errors = True
        if len(request.POST['lname']) < 2:
            messages.error(request,'Last name must be at least 2 characters!')
            errors = True
        if not request.POST['lname'].isalpha():
            messages.error(request,"Last name should be alpha only")
            errors = True
        if len(request.POST['email']) < 1:
            messages.error(request,'Email cannot be empty!')
            errors = True
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request,'Invalid Email Address!')
            errors = True
        if len(request.POST['pass']) < 8:
            messages.error(request,'Password should be at least 8 characters!')
            errors = True
        if request.POST['pass'] != request.POST['pass_confirm']:
            messages.error(request,'Password does not match password confirmation')
            errors = True
        #validate that email doesn't already exist in database
        user = User.objects.filter(email=request.POST['email'])
        if len(user) != 0:
            messages.error(request,"This email has already been registered")
            errors = True

        return errors


        #END validation code here
        ###########################################################

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)   
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name,self.last_name)

class Author(models.Model):
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    def __repr__(self):
        return "<Author object: {}>".format(self.author)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,related_name="books")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    def __repr__(self):
        return "<Book object: {}>".format(self.title)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User,related_name="reviews")
    book = models.ForeignKey(Book,related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    def __repr__(self):
        return "<Review object: {}>".format(self.review)