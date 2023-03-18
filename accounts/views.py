from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate

# Create your views here.
def welcome(request):
    return HttpResponse("<h3>Welcome to our Homepage</h3>")

def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Hello, You are now logged in as <b>{username}</b>.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error) 
            
    else:
        form = LoginForm()
    context={
        "form":form
    }
    return render(request, 'login.html', context=context)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.cleaned_data['username'] = username.lower()
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('account:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegistrationForm()
        
    context={
        "form":form
    }

    return render(request=request, template_name="register.html", context=context)