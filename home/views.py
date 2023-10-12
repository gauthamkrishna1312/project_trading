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
        print(models.Payment.objects.filter(user=request.user).exists())
        if request.user.is_superuser:
                return redirect("/moderator/index")
        
        user_plan = models.User_plan.objects.filter(user=request.user)
        payment = models.Payment.objects.filter(user=request.user)
        withdraw = models.Withdraw.objects.filter(user=request.user)

        context = {
            "user_plans": user_plan,
            "payments": payment,
            "withdraws": withdraw,
        }
        
        return render(request, 'index.html', context=context)

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

        user_plan = models.User_plan()
        user_plan.user = request.user
        user_plan.invested_amount = "0"
        user_plan.plan = models.Plans.objects.get(id=1)
        user_plan.plan_status = "Inactive"
        user_plan.plan_profit = "0"
        user_plan.save()

        return render(request, "index.html")

class Login_view(View):

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        
        uname = request.POST["login_uname"]
        passw = request.POST["login_passw"]
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
        return redirect("/login")



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
    
    def post(self, request):

        withdraw_name = request.POST["withdraw_name"]
        withdraw_amount = request.POST["withdraw_amount"]

        if int(withdraw_amount) < 10:

            messages.info(request, "minimum amount is 10")
            return redirect("/withdraw")

        user_plan = models.User_plan.objects.get(user=request.user)

        if int(withdraw_amount) > int(user_plan.plan_profit):

            messages.info(request, "insufficient fund")
            return redirect("/withdraw")

        withdraw = models.Withdraw()
        withdraw.user = request.user
        withdraw.withdraw_amount = withdraw_amount
        withdraw.withdraw_status = "pending"
        withdraw.save()

        return redirect("/")

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
            payment.transaction_status = "pending"
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
            action = kwargs["action"]

            payment = models.Payment.objects.get(id=payment_id)
            if action == "approve":
                if payment.transaction_status == "Approved":
                    
                    messages.info(request, "already approved")
                    return redirect("/moderator/payments/approved")
                
                if models.User_plan.objects.filter(user=payment.user).exists() == True:

                    user_plan = models.User_plan.objects.get(user=payment.user)
                    user_plan.invested_amount = str(int(user_plan.invested_amount) + int(payment.transaction_amount))
                    plan = self.get_plan(user_plan.invested_amount)
                    user_plan.plan = plan
                    user_plan.plan_status = "Active"
                    user_plan.save()

                payment.transaction_status = "approved"
                payment.save()

                return redirect("/moderator/payments/approved")

            elif action == "reject":

                payment.transaction_status = 'rejected'
                payment.save()

                return redirect("/moderator/payments/rejected")

        else:
            status = kwargs["status"]
            context = {
                "payments": models.Payment.objects.all(),
                "status": status,
            }

            return render(request, "admpayments.html", context=context)
        
    def get_plan(self, amount: int):

        plan_db = models.Plans.objects.all()
        for plan in plan_db:
            if int(amount) >= int(plan.plan_min_price) and int(amount) < int(plan.plan_max_price):
                return plan

class Admwithdraw_view(View):
    
    def get(self,request, **kwargs):

        if "id" in kwargs:

            withdraw_id = kwargs["id"]
            action = kwargs["action"]

            withdraw = models.Withdraw.objects.get(id=withdraw_id)

            if action == "done":
                
                user_plan = models.User_plan.objects.get(user=withdraw.user)
                user_plan.plan_profit = str(int(user_plan.plan_profit) - int(withdraw.withdraw_amount))
                user_plan.save()
                withdraw.withdraw_status = "done"
                withdraw.save()

                return redirect("/moderator/withdraw/done")

        status = kwargs["status"]
        context = {
            "withdraws": models.Withdraw.objects.all(),
            "status": status,
        }

        return render(request, 'admwithdraw.html', context=context)

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
