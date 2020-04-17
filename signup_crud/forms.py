from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
import re

User = get_user_model()

class SingupForm(forms.Form):  
    username =forms.CharField(widget = forms.TextInput(attrs = {
        "class":"form-control input-lg"
        }))
    email=forms.EmailField(widget = forms.TextInput(attrs = {
        "class":"form-control input-lg"
        }))
    first_name = forms.CharField(widget = forms.TextInput(attrs = {
        "class":"form-control input-lg"
        }))
    last_name  = forms.CharField(widget = forms.TextInput(attrs = {
        "class":"form-control input-lg"
        }))
    password   = forms.CharField(widget = forms.PasswordInput(attrs = {
        "class":"form-control input-lg"
        }), label='Password')
    password2  = forms.CharField(widget = forms.PasswordInput(attrs = {
        "class":"form-control input-lg"
        }), label='Confirm Password')
    
    is_staff   = forms.BooleanField()
   # is_active  = forms.BooleanField()

    def clean(self):
        data       = self.cleaned_data
        password   = data.get('password')
        password2  = data.get('password2')

        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise forms.ValidationError('''Passwords must contain: a minimum of 1 lower case letter [a-z],
                                          a minimum of 1 upper case letter [A-Z] and a minimum of 1 special
                                         charecture.''')

        if password2 != password:
        	raise forms.ValidationError("Passwords do not match")

        return data

    def clean_first_name(self):
        data        = self.cleaned_data
        first_name  = data.get('first_name')

        if(len(first_name)<=2):
            raise forms.ValidationError("First Name should be atleast 3 charectures.")

        elif not first_name.isalpha():
            raise forms.ValidationError("First Name should be alpha charectures.")

        return first_name           


    def clean_email(self):
        data      = self.cleaned_data
        email     = data.get('email')
        qs        = User.objects.filter(email=email)
        if qs.exists():
            #raise forms.ValidationError("Email is registered")
            msg = """This Email is registered, would you like to <a href="{link}">login</a>?
            """.format(link='/login')
            raise forms.ValidationError(mark_safe(msg))
        return email

    def clean_username(self):
        data      = self.cleaned_data
        username     = data.get('username')
        qs        = User.objects.filter(username=username)
        if qs.exists():
            msg = """This username is registered, would you like to <a href="{link}">login</a>?
            """.format(link='/singup_crud/login/')
            raise forms.ValidationError(mark_safe(msg))
        return username

class LoginForm(forms.Form):
    username    = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data      = self.cleaned_data
        username  = data.get("username")
        password  = data.get("password")
        qs        = User.objects.filter(username=username)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ## not active, check email activation
                raise forms.ValidationError("This user is inactive.")
        elif not qs.exists():
            # User email in not registred
            msg = """This username is not registered, would you like to <a href="{link}">signup</a>?
            """.format(link='/singup_crud/create/')
            raise forms.ValidationError(mark_safe(msg))

        return data

        