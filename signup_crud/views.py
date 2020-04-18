from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from signup_crud.forms import SingupForm, LoginForm
from django.utils.http import is_safe_url
import re

# Create your views here.
User = get_user_model()

def singup_view(request):
	form     = SingupForm(request.POST or None)
	context  = {
        "form"        : form,
        "is_register" : False
    }
	if request.method == "POST" and form.is_valid():
		data       = form.cleaned_data
		username   = data.get("username")
		email      = data.get("email")
		first_name = data.get("first_name")
		last_name  = data.get("last_name")
		password   = data.get("password")
		is_staff   = data.get("is_staff")

		extra_fields        = {
		"first_name" : first_name,
		"last_name"  : last_name,
		"is_staff"   : is_staff,
		"is_active"  : True

		}
		new_user            = User.objects.create_user(username, email, password, **extra_fields)
		form     = SingupForm()
		context = {
            "form"        : form,
            "is_register" : True
        }
	return render(request, 'index.html', context)

def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form"     : form,
        "is_invalid" : False
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
    	data      = form.cleaned_data
    	username  = data.get("username")
    	password  = data.get("password")
    	user      = authenticate(request, username=username, password=password)
    	if user is not None:
    		login(request, user)
    		if is_safe_url(redirect_path, request.get_host()):
    			print(redirect_path)
    			return redirect(redirect_path)
    		else:
    			return redirect("/")
    	else:
            # Return an 'invalid login' error message.
            form = LoginForm()
            context = {
               "form"     : form,
               "is_invalid" : True
            }
    return render(request, "login.html", context)

def users_view(request):
	if not is_admin_user(request):
		users = []
		msg = """You don't have specific permsission to access this page, 
		    would you like to Admin Login?
		    Admin Credentials: username= vishavjeet, Password= 12345678"""
	else:
		users = User.objects.all()
		msg   = ''
	return render(request,"user-list.html",{'users':users, 'msg':msg})

def destroy(request, id):
	users = User.objects.get(pk=id)
	users.delete()
	return redirect("/singup_crud/")

def edit_view(request, id):
	user = get_object_or_404(User, pk=id)
	#form      = SingupForm(request.POST or None, instance = user)
	error_msg  = ''
	is_updated = False
	if request.method == "POST":
		data               = request.POST
		user.username      = data.get("username")
		user.email         = data.get("email")
		user.first_name    = data.get("first_name")
		user.last_name     = data.get("last_name")
		user.is_staff      = data.get("is_staff")
		is_change_password = data.get("is_change_password")
		if is_change_password:
			password     = data.get("password")
			password2     = data.get("password2")
			if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
				error_msg = "Passwords contain minimum of 8 charectures"
			elif password2 != password:
				error_msg = "Passwords do not match"
			else:
				user.set_password(password)
				is_updated = True
				user.save()
		else:
			is_updated = True
			user.save()
	context   = {
	    "user"       : user,
	    'error_msg'  : error_msg,
	    'is_updated' : is_updated
	}
	return render(request, "edit.html", context)

def show_view(request, id):
	user = get_object_or_404(User, pk=id)
	return render(request,"show.html",{'user':user})

def home_view(request):
	return redirect("/singup_crud")

def logout_view(request):
    logout(request)
    return redirect("/")

def is_admin_user(request):
	if request.user.is_authenticated:
		if request.user.groups.filter(name='admin').exists():
			return True
		return False
	return False





		
		

