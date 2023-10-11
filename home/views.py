from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from . import models

# Create your views here.
class Index_view(View):
    
    def get(self, request):
        return render(request, 'index.html')

class Contact_view(View):

    def get(self, request):
        return render(request, 'contact.html')

class Yourplan_view(View):

    def get(self, request):

        user_plan = models.User_plan.objects.filter(user=request.user)
        context = {
            "user_plans": user_plan,
        }
        return render(request, 'yourplan.html', context=context)

class Newplan_view(View):

    def get(self, request):

        context = {
            "plans": models.Plans.objects.all(),
        }
        return render(request, 'newplan.html', context=context)

class Profit_view(View):

    def get(self,request):
        return render(request, 'profit.html')

class Withdraw_view(View):

    def get(self,request):
        return render(request, 'withdraw.html')

class Refer_view(View):
    
    def get(self,request):
        return render(request, 'refer.html')

class Payment_view(View):

    def get(self,request):
        return render(request, 'payment.html')
    
class Profile_view(View):

    def get(self,request):
        return render(request, 'profile.html')

class History_view(View):

    def get(self,request):
        return render(request, 'history.html')

class Admindex_view(View):

    def get(self,request):
        return render(request, 'admindex.html')

class Admreg_view(View):

    def get(self,request):

        context = {
            "members": User.objects.all(),
        }

        return render(request, 'admreg.html', context=context)

class Admregact_view(View):

    def get(self,request):
        return render(request, 'admregact.html')

class Admpayments_view(View):

    def get(self,request):
        return render(request, 'admpayments.html')

class Admwithdraw_view(View):

    def get(self,request):
        return render(request, 'admwithdraw.html')

class Admaddplan_view(View):

    def get(self,request):
        return render(request, 'admaddplan.html')
    
class Admeditplan_view(View):

    def get(self,request):
        return render(request, 'admeditplan.html')
    
class Admaddprofit_view(View):

    def get(self,request):
        return render(request, 'admaddprofit.html')

class Signup_view(View):

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["signup_email"]
        uname = request.POST["signup_uname"]
        passw = request.POST["signup_passw"]

        user = User(first_name=fname, last_name=lname,username=uname, email=email)
        user.set_password(passw)
        user.save()
        authenticate(username=uname, password=passw)
        login(request, user)

        return render(request, "index.html")

class Login_view(View):

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        
        uname = request.POST["login_uname"]
        passw = request.POST["login_passw"]
        print(uname)
        user = authenticate(username=uname, password=passw)
        
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        
class Logout_view(View):

    def get(self, request):

        logout(request)
        messages.info(request, "logged out")
        return render(request, "index.html")
