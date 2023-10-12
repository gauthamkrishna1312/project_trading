from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

from . import models

# Create your views here.
class Index_view(View):
    
    def get(self, request):

        if models.User_plan.objects.filter(user=request.user).exists() == True:
            user_plan = models.User_plan.objects.get(user=request.user)

            if int(user_plan.invested_amount) <= 1000:
                plan_name = "plan1"
            if int(user_plan.invested_amount) > 1000 and int(user_plan.invested_amount) <= 5000:
                plan_name = "plan2"

            plan = models.Plans.objects.get(plan_name=plan_name)

            context = {
                "user_plan": user_plan,
                "plan": plan,
            }
            return render(request, 'index.html', context=context)
        return render(request, 'index.html')

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
            if request.user.is_superuser:
                return redirect("/moderator/index")
            return render(request, "index.html")
        
class Logout_view(View):
    
    def get(self, request):

        logout(request)
        messages.info(request, "logged out")
        return redirect("home")



class Contact_view(View):
    
    def get(self, request):
        return render(request, 'contact.html')

class Yourplan_view(View):
    
    def get(self, request):

        user_plan = models.User_plan.objects.filter(user=request.user)
        context = {
            "user_plan": user_plan,
        }
        return render(request, 'yourplan.html', context=context)

class Newplan_view(View):
    
    def get(self, request):

        context = {
            "plans": models.Plans.objects.all(),
        }
        return render(request, 'newplan.html', context=context)
    
class Editplan_view(View):

    def get(self, request, plan_id):

        context = {
            "plan": models.Plans.objects.get(id=plan_id)
        }
        return render(request, "admaddplan.html", context=context)
    
    def post(self, request, plan_id):
        
        plan_name = request.POST["plan_name"]
        plan_price = request.POST["plan_price"]
        plan_min_percentage = request.POST["plan_min_percentage"]
        plan_max_percentage = request.POST["plan_max_percentage"]
        plan_min_profit = request.POST["plan_min_profit"]
        plan_max_profit = request.POST["plan_max_profit"]

        plan = models.Plans.objects.get(id=plan_id)
        plan.plan_name = plan_name
        plan.plan_price = plan_price
        plan.plan_min_percentage = plan_min_percentage
        plan.plan_max_percentage = plan_max_percentage
        plan.plan_min_profit = plan_min_profit
        plan.plan_max_profit = plan_max_profit
        plan.save()

        messages.success(request, "Plan changed")
        return redirect("adm_edit_plan")

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


        # if models.User_plan.objects.filter(user=request.user).exists() == True:
            # messages.info(request, "plan already exists")
            # return redirect("yourplan")

        return render(request, 'payment.html')
    
    def post(self, request):
        
        transaction_name = request.POST["transaction_name"]
        transaction_id = request.POST["transaction_id"]
        amount = request.POST["amount"]

        
        if int(amount) < 100:
            messages.info(request, "minimum amount is 100")
            return render(request, "payment.html")
        if float(str(int(amount)/50).split(".")[1]) > 0:
            messages.info(request, "only multiples of 50")
            return render(request, "payment.html")
        else:

            payment = models.Payment()
            payment.user = request.user
            payment.transaction_name = transaction_name
            payment.transaction_id = transaction_id
            payment.transaction_amount = amount
            payment.transaction_status = "processing"
            payment.save()
            messages.info(request, "payment is requested")

            return redirect("home")
    
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
    
    def get(self,request, **kwargs):
        
        if "id" in kwargs:
            
            payment_id = kwargs["id"]

            payment = models.Payment.objects.get(id=payment_id)
            if models.User_plan.objects.filter(user=payment.user).exists() == False:

                user_plan = models.User_plan()
                user_plan.user = payment.user
                user_plan.invested_amount = payment.transaction_amount
                user_plan.plan_status = "Active"
                user_plan.plan_profit = "0"
                user_plan.save()
            
            if models.User_plan.objects.filter(user=payment.user).exists() == True:

                user_plan = models.User_plan.objects.get(user=payment.user)
                user_plan.invested_amount = str(int(user_plan.invested_amount) + int(payment.transaction_amount))
                user_plan.save()

            payment.transaction_status = "Approved"
            payment.save()

            return redirect("/moderator/payments/")

        else:
            context = {
                "payments": models.Payment.objects.all()
            }

            return render(request, "admpayments.html", context=context) 

class Admwithdraw_view(View):
    
    def get(self,request):
        return render(request, 'admwithdraw.html')

class Admaddplan_view(View):
    
    def get(self,request):
        return render(request, 'admaddplan.html')
    
    def post(self, request):

        plan_name = request.POST["plan_name"]
        plan_price = request.POST["plan_price"]
        plan_min_percentage = request.POST["plan_min_percentage"]
        plan_max_percentage = request.POST["plan_max_percentage"]
        plan_min_profit = request.POST["plan_min_profit"]
        plan_max_profit = request.POST["plan_max_profit"]

        plan = models.Plans()
        plan.plan_name = plan_name
        plan.plan_price = plan_price
        plan.plan_min_percentage = plan_min_percentage
        plan.plan_max_percentage = plan_max_percentage
        plan.plan_min_profit = plan_min_profit
        plan.plan_max_profit = plan_max_profit
        plan.save()

        messages.success(request, "Plan created")
        return redirect("adm_edit_plan")

    
class Admeditplan_view(View):
    
    def get(self,request):

        context = {
            "plans": models.Plans.objects.all()
        }

        return render(request, 'admeditplan.html', context=context)
    
class Admaddprofit_view(View):
    
    def get(self,request):
        return render(request, 'admaddprofit.html')
