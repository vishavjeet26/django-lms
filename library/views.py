# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from library.models import Author, Books, Student, Librarian
from library.forms import UserForm, StudentForm, BookForm, StaffForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.db.models import Q

from django.views.generic import ListView, CreateView
from django.views import View

from lms_api.permissions import (IsAdminOrReadOnly,IsAdminStaffOrReadOnly, 
    IsAdminStaffStudentOrReadOnly)

import logging

# instance of logging class
logger = logging.getLogger(__name__)
# logging format
format='%(asctime)s : %(levelname)-4s: %(threadName)-4s : %(pathname)-4s : %(lineno)d : %(funcName)-4s: %(message)s'
# Basic Logging Configuration without settings.py file
logging.basicConfig(filename = 'logs/student.log', level=logging.DEBUG, format=format)

# Create class/function views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                query = request.GET.get('q')
            except ValueError:
                #logging.debug('URLString not valid')
                query = None
            if query:
                q_type = request.GET.get('type')
                if q_type == 'author':
                    detail = Books.objects.filter(author__fullname__icontains=query)
                if q_type == 'title':
                    detail = Books.objects.filter(title__icontains=query)
                if q_type == 'isbn':
                    detail = Books.objects.filter(isbn=query)
                if q_type == 'users':
                    detail = Student.objects.filter(fullname__icontains=query) or Student.objects.filter(enrollment_no__icontains=query) \
                    or Librarian.objects.filter(fullname__icontains=query) or Librarian.objects.filter(librarian_id__icontains=query)
                if not detail:
                    #logging.debug('No results found!')
                    detail = ['No results found!']
                return render(request, 'library/index.html', {'detail': detail})
            return render(request, 'library/index.html', {})
        else:
          #logging.debug('UnAuthenticated user trying to access book')  
          return redirect('/singup_crud/login/')


class CreateUserView(View):

    def get(self, request):
        if is_admin_user(request):
            form = UserForm
            return render(request, 'library/adminpage.html', {'form':form})
        return HttpResponse("You don't have specific permsission to access this page.")      

    def post(self, request, *args, **kwargs):

        if is_admin_user(request):
            form = UserForm(request.POST)
            if form.is_valid():
                detail = form.save(commit=False)
                detail.save()
                if request.POST.get('acctype') == 'student':
                    return redirect('create_student', username=detail.username, admin=request.user.username)
                else:
                    return redirect('create_staff', username=detail.username, admin=request.user.username)
            return render(request, 'library/adminpage.html', {'form':form})
        return redirect('/singup_crud/login/')

class StudentDashboardView(ListView):
    template_name = "library/student_dashboard.html"
    queryset      = Books.objects.filter(request_issue=True) 
    context_object_name = 'detail'
    paginate_by = 10
    permission_classes = (IsAdminStaffStudentOrReadOnly, )
    logging.info('Student Dashboard')        

class CreateStudentView(View):
    def get(self, request , username, admin):
        if is_admin_user(request):
            form = StudentForm
            return render(request, 'library/createstudent.html', {'form':form})
        logging.warning('You don`t have specific permsission to access this page.') 
        return HttpResponse("You don't have specific permsission to access this page.")      

    def post(self, request, username, admin, *args, **kwargs):
        if is_admin_user(request):
            form = StudentForm(request.POST)
            user_instance = get_object_or_404(User, username=username)
            if user_instance is None:
                logging.critical('User instance not found!')  
            if form.is_valid():
                detail = form.save(commit=False)
                detail.user = user_instance
                detail.fullname = detail.first_name + ' ' + detail.last_name
                detail.save()
                detail.user.groups.add(Group.objects.get(name='student'))
                logging.info('User Created, User :'+detail.fullname) 
                return redirect('create_user')
            logging.error('Something wrong!')    
            return render(request, 'library/createstudent.html', {'form':form})
        logging.warning('UnAuthenticated user try to post request')     
        return redirect('/singup_crud/login/')                      

def staff_issue(request):
    if request.user.is_authenticated:    
        if request.user.groups.filter(Q(name='staff') | Q(name='admin')).exists():
            detail = Books.objects.filter(request_issue=True)
            return render(request, 'library/staff_issue.html', {'detail': detail})
        return HttpResponse("You don't have specific permsission to access this page.")    
    return redirect('/singup_crud/login/')

def staff_addbook(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(Q(name='staff') | Q(name='admin')).exists():        
            if request.method == 'POST':
                form = BookForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.save()
                    form = BookForm
                    return render(request, 'library/staff_addbook.html', {'form': form})
            else:
                form = BookForm
            return render(request, 'library/staff_addbook.html', {'form': form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('/singup_crud/login/')

def change_request_issue(request):
    request_issue = request.GET.get('request_val')
    bookid = request.GET.get('bookid')
    email = request.GET.get('usermail')
    myobject = Books.objects.filter(book_id=bookid)
    if myobject.exists():
        myobject.update(request_issue=request_issue, email=email)
        boolval = 'True'
    else:
        boolval = 'False'
    data = {
        'valdb': boolval
    }
    return JsonResponse(data)

def change_issue_status(request):
    issue_status = request.GET.get('issue_val')
    bookid = request.GET.get('bookid')
    myobject = Books.objects.filter(book_id=bookid)
    duedate = datetime.now().date() + timedelta(days=14)
    returndate = datetime.now().date()
    issuedate = datetime.now().date()
    email_subject = 'Book Issue Notice'
    recipient_mail = myobject[0].email.encode('utf-8')
    if myobject.exists():
        myobject.update(issue_status=issue_status)
        if issue_status == 'True':
            myobject.update(issue_date=issuedate, due_date=duedate, return_date=None, fine=0)
            email_body = 'The following book has been issued to you.\n\n'\
                 'Book: ' + myobject[0].title.encode('utf-8') + '\n\n'\
                 'Due Date: ' + myobject[0].due_date.strftime('%d/%m/%Y') + '\n'
            send_mail(email_subject, email_body, "vishavjeet <python.ds.com@gmail.com>", [recipient_mail])
        if issue_status == 'False':
            fine = (returndate - issuedate).days
            myobject.update(return_date=returndate, due_date=None, fine=fine)
        boolval = 'True'
    else:
        boolval = 'False'
    data = {
        'valdb': boolval
    }
    return JsonResponse(data)


def create_staff(request, username, admin):
    if request.user.username == admin:
        if request.user.groups.filter(name='admin').exists():        
            user_instance = get_object_or_404(User, username=username)
            if request.method == "POST":
                form = StaffForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = user_instance
                    detail.save()
                    detail.user.groups.add(Group.objects.get(name='staff'))
                    return redirect('create_user')
            else:
                form = StaffForm
            return render(request, 'library/createstaff.html', {'form':form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('/singup_crud/login/')

def logout_view(request):
    logout(request)
    return redirect("/")

def is_admin_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            print("Admin login...")
            return True
    return False   

"""
Custom permission to only allow Staff of an object to create book, see all books,
assign book and submit ot user.
"""
def is_admin_staff_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(Q(name='admin') | Q(name='staff')).exists():
            print("Staff login...")
            return True
    return False        

"""
Custom permission to only allow admin, staff and student of an object to see all books,
check book status, create assign request
"""
def is_admin_staff_student_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(Q(name='admin') | Q(name='staff') | Q(name='student')).exists():
            print("student login...")
            return True
    return False
