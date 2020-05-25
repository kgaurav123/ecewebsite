from django.shortcuts import render, HttpResponseRedirect, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm,ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from .models import *

def index(request):
    notice = Notice.objects.all()
    print(notice)
    return render(request,'ece/home.html',{'notice':notice})

def signup(request):
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password=form.cleaned_data.get('password1')
			return redirect('login')
	else:
		form=UserForm()
	args={'form': form}
	return render(request,'ece/signup.html',args)

def login_view(request):
	message='Log In'
	if request.method=='POST':
		_username=request.POST['username']
		_password=request.POST['password']
		user=authenticate(username=_username,password=_password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('/update')
			else:
				message='Not Activated'
		else:
			message='Invalid Login'
	context={'message':message}
	return render(request,'ece/login.html',context)

@login_required
def logout_view(request):
	logout(request)
	return redirect('/login/')


@login_required
def update_profile(request):
	message='Update'
	if request.method=='POST':
		form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid:
			form.save()

			return redirect('/logout')
		else:
			message='Image size should be less tahn 1mb'
			return redirect('/update')
	else:
		form=ProfileUpdateForm()
	return render(request,'ece/formupdate.html',{'form':form,'message':message})

def member_list(request):
	first_year=Profile.objects.filter(year='1').order_by('-user')
	second_year=Profile.objects.filter(year='2').order_by('-user')
	third_year=Profile.objects.filter(year='3').order_by('-user')
	fourth_year=Profile.objects.filter(year='4').order_by('-user')
	context = {'first_year':first_year,'second_year':second_year,'third_year':third_year,'fourth_year':fourth_year}
     
	return render(request,'ece/members.html',context)