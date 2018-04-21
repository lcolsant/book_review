# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from .models import UserManager
from .models import Book
from .models import Author
from .models import Review
import bcrypt

def index(request):
  
    if 'id' in request.session.keys():
        return redirect('/books')
    
    return render(request,'book_review/index.html')

def register(request):
    #validate data first
    errors = User.objects.validate(request)
    if (errors):
        print 'Invalid input'
        return redirect('/')
    else:
        #hash password and add to db
        hash_password = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())
        print hash_password
        User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],password=hash_password)
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
    return redirect('/books')

def login(request):
    email = request.POST['email']
    password = request.POST['pass']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request,"User not recognized")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            print 'password matches'
            request.session['id'] = user[0].id
            return redirect('/books')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')


def books(request):

    if request.session.get('id') == None:
        return redirect('/')

    context = {
        'user':User.objects.get(id=request.session['id']),
        'reviews':Review.objects.all().order_by('-created_at')[:3],
        'all_books':Book.objects.all()

    }
    
    return render(request, 'book_review/books.html',context)

def add_book(request):
    return render(request,'book_review/add.html')

def process(request):

    author = Author.objects.create(author=request.POST['author'])
    book = Book.objects.create(title=request.POST['title'],author=author)
    Review.objects.create(review=request.POST['review'],rating=request.POST['rating'], reviewer=User.objects.get(id=request.session['id']),book=book)
    
    return redirect('/books/{}'.format(book.id) )

def show(request,id):
     book = Book.objects.get(id=id)
     reviews = Review.objects.filter(book=book).order_by('-created_at')
     context = {
         'book':book,
         'reviews':reviews
     }
     return render(request,'book_review/show.html',context)


def show_user(request,id):
     user = User.objects.get(id=id)
     count = user.reviews.count()
     user_reviews = Review.objects.filter(reviewer=user)
     context = {
         'user':user,
         'count':count,
         'user_reviews':user_reviews
     }
     
     return render(request,'book_review/show_user.html',context)

def add_review(request,id):
    book = Book.objects.get(id=id)
    Review.objects.create(review=request.POST['review'],rating=request.POST['rating'], reviewer=User.objects.get(id=request.session['id']),book=book)
    messages.success(request, "Successfully added review.")
    return redirect('/books/{}'.format(id))

def logout(request):
    request.session.clear()
    return redirect('/')