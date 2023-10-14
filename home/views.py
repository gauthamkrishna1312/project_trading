from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from . import models


class Index_view(View):

    def get(self, request):

        if request.user.is_superuser:
                return redirect("/moderator/dashboard/")
        
        return redirect("/dashboard")

class Dashboard_view(View):
    
    def get(self, request):
        
        user_plans = models.User_plan.objects.filter(user=request.user)
        payments = models.Payment.objects.filter(user=request.user)
        withdraws = models.Withdraw.objects.filter(user=request.user)

        context = {
            "user_plans": user_plans,
            "payments": payments,
            "withdraws": withdraws,
        }
        
        return render(request, 'user/index.html', context=context)

class Signup_view(View):

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["signup_email"]
        uname = request.POST["signup_uname"]
        passw1 = request.POST["signup_passw1"]
        passw2 = request.POST["signup_passw2"]

        temp_context = {
                "fname": fname,
                "lname": lname,
                "email": email,
                "uname": uname
            }
        
        try:
            validate_password(passw1)
        except ValidationError:
            messages.error(request, "password validation error")
            return render(request, "signup.html", context=temp_context)

        if passw1 != passw2:

            messages.error(request, "password didnt match")
            return render(request, "signup.html", context=temp_context)

        user = User(first_name=fname, last_name=lname,username=uname, email=email)
        user.set_password(passw1)
        user.save()
        authenticate(username=uname, password=passw1)
        login(request, user)

        user_plan = models.User_plan()
        user_plan.user = request.user
        user_plan.invested_amount = "0"
        user_plan.plan = models.Plans.objects.get(id=1)
        user_plan.user_status = "Inactive"
        user_plan.user_profit = "0"
        user_plan.save()

        messages.success(request, "Signup Successful")
        return redirect("/dashboard")

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
                return redirect("/moderator/dashboard/")
            return redirect(f"/dashboard")
        else:
            messages.error(request, "user name or password is invalid")
            return redirect("/login")
        
class Logout_view(View):
    
    def get(self, request):

        logout(request)
        messages.info(request, "logged out")
        return redirect("/login")



class Contact_view(View):
    
    def get(self, request):
        return render(request, 'user/contact.html')

# class Yourplan_view(View):
    
#     def get(self, request):

#         user_plan = models.User_plan.objects.filter(user=request.user)
#         context = {
#             "user_plan": user_plan,
#         }
#         return render(request, 'yourplan.html', context=context)

class Plans_view(View):
    
    def get(self, request):

        context = {
            "plans": models.Plans.objects.all(),
        }
        return render(request, 'user/plans.html', context=context)

class Profit_view(View):
    
    def get(self,request):

        user_plan = models.User_plan.objects.get(user=request.user)
        context = {
            "user_plan": user_plan,
        }

        return render(request, 'user/profit.html', context=context)

class Withdraw_view(View):
    
    def get(self,request):
        return render(request, 'user/withdraw.html')
    
    def post(self, request):

        withdraw_name = request.POST["withdraw_name"]
        withdraw_amount = request.POST["withdraw_amount"]
        wallet_id = request.POST.get("wallet_id", None)
        account_no = request.POST.get("account_no", None)
        ifsc_code = request.POST.get("ifsc_code", None)

        if int(withdraw_amount) < 10:

            messages.info(request, "minimum amount is 10")
            return redirect("/withdraw")

        user_plan = models.User_plan.objects.get(user=request.user)

        if int(withdraw_amount) > int(user_plan.user_profit):

            messages.error(request, "insufficient fund")
            return redirect("/withdraw")

        withdraw = models.Withdraw()
        withdraw.user = request.user
        withdraw.withdraw_amount = withdraw_amount
        withdraw.account_name = withdraw_name
        withdraw.account_no = account_no
        withdraw.wallet_id = wallet_id
        withdraw.ifsc_code = ifsc_code
        withdraw.withdraw_status = "pending"
        withdraw.save()

        return redirect("/dashboard")

class Refer_view(View):
    
    def get(self,request):
        return render(request, 'user/refer.html')

class Payment_view(View):
    
    def get(self,request):

        return render(request, 'user/payment.html')
    
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
            return redirect("/dashboard")
    
class Profile_view(View):
    
    def get(self,request):
        return render(request, 'user/profile.html')

class History_view(View):
    
    def get(self,request, **kwargs):

        action = kwargs["action"]
        payments = models.Payment.objects.filter(user=request.user)
        withdraw = models.Withdraw.objects.filter(user=request.user)
        addprofit = models.Addprofit.objects.filter(user=request.user)
        context = {
            "payments": payments,
            "withdraws": withdraw,
            "addprofits": addprofit,
            "action": action,
        }

        return render(request, 'user/history.html', context=context)




class ModDashboard_view(View):
    
    def get(self,request):
        return render(request, 'mod/index.html')

class ModMembers_view(View):
    
    def get(self, request,**kwargs):

        if "status" in kwargs:
            context = {
                "members": models.User_plan.objects.filter(user_status=kwargs["status"]),
            }

            return render(request, 'mod/ .html', context=context)
        
        context = {
            "members": User.objects.all(),
        }

        return render(request, 'mod/members.html', context=context)

# class Admregact_view(View):
    
#     def get(self,request):

#         user_plans = models.User_plan.objects.filter(user_status="Active")
#         ids = range(1,len(user_plans)+1)
#         context = {
#             "user_plans": user_plans,
#             "ids": ids,
#         }

#         return render(request, 'mod/admregact.html', context=context)

class ModPayments_view(View):
    
    def get(self,request, **kwargs):
        
        if "id" in kwargs:
            
            payment_id = kwargs["id"]
            action = kwargs["action"]

            payment = models.Payment.objects.get(id=payment_id)
            if action == "approve":
                if payment.transaction_status == "Approved":
                    
                    messages.error(request, "already approved")
                    return redirect("/moderator/payments/approved")
                
                if models.User_plan.objects.filter(user=payment.user).exists() == True:

                    user_plan = models.User_plan.objects.get(user=payment.user)
                    user_plan.invested_amount = str(int(user_plan.invested_amount) + int(payment.transaction_amount))
                    plan = self.get_plan(user_plan.invested_amount)
                    user_plan.plan = plan
                    user_plan.user_status = "Active"
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

            return render(request, "mod/payments.html", context=context)
        
    def get_plan(self, amount):

        plan_db = models.Plans.objects.all()
        for plan in plan_db:
            if int(amount) >= int(plan.plan_min_price) and int(amount) < int(plan.plan_max_price):
                return plan

class ModWithdraw_view(View):
    
    def get(self,request, **kwargs):

        if "id" in kwargs:

            withdraw_id = kwargs["id"]
            action = kwargs["action"]

            withdraw = models.Withdraw.objects.get(id=withdraw_id)

            if action == "done":
                
                user_plan = models.User_plan.objects.get(user=withdraw.user)
                user_plan.user_profit = str(int(user_plan.user_profit) - int(withdraw.withdraw_amount))
                user_plan.save()
                withdraw.withdraw_status = "done"
                withdraw.save()

                return redirect("/moderator/withdraw/done")
            
            elif action == "rejected":

                withdraw.withdraw_status = "rejected"
                withdraw.save()

                return redirect("/moderator/withdraw/rejected")

        status = kwargs["status"]
        context = {
            "withdraws": models.Withdraw.objects.all(),
            "status": status,
        }

        return render(request, 'mod/withdraw.html', context=context)

class ModAddPlan_view(View):
    
    def get(self,request):
        return render(request, 'mod/addplan.html')
    
    def post(self, request):

        plan_name = request.POST["plan_name"]
        plan_min_percentage = request.POST["plan_min_percentage"]
        plan_max_percentage = request.POST["plan_max_percentage"]
        plan_min_price = request.POST["plan_min_price"]
        plan_max_price = request.POST["plan_max_price"]

        if self.get_plan(plan_min_price) is not None:

            messages.error(request, "plan alredy exists")
            return redirect("/moderator/plans")

        plan = models.Plans()
        plan.plan_name = plan_name
        plan.plan_min_percentage = plan_min_percentage
        plan.plan_max_percentage = plan_max_percentage
        plan.plan_min_price = plan_min_price
        plan.plan_max_price = plan_max_price
        plan.save()

        messages.success(request, "Plan created")
        return redirect("/moderator/plans")
    
    def get_plan(self, amount):

        plan_db = models.Plans.objects.all()
        for plan in plan_db:
            if int(amount) >= int(plan.plan_min_price) and int(amount) < int(plan.plan_max_price):
                return plan
            else:
                return None

    
class ModPlans_view(View):
    
    def get(self,request):

        context = {
            "plans": models.Plans.objects.all()
        }

        return render(request, 'mod/plans.html', context=context)
    
class ModEditPlan_view(View):

    def get(self, request, plan_id):

        context = {
            "plan": models.Plans.objects.get(id=plan_id),
            "edit": None,
        }
        return render(request, "mod/addplan.html", context=context)
    
    def post(self, request, plan_id):
        
        plan_name = request.POST["plan_name"]
        plan_min_percentage = request.POST["plan_min_percentage"]
        plan_max_percentage = request.POST["plan_max_percentage"]
        plan_min_price = request.POST["plan_min_price"]
        plan_max_price = request.POST["plan_max_price"]

        plan = models.Plans.objects.get(id=plan_id)
        plan.plan_name = plan_name
        plan.plan_min_percentage = plan_min_percentage
        plan.plan_max_percentage = plan_max_percentage
        plan.plan_min_price = plan_min_price
        plan.plan_max_price = plan_max_price
        plan.save()

        messages.success(request, "Plan changed")
        return redirect("/moderator/plans")
    
class ModAddProfit_view(View):
    
    def get(self,request):
        return render(request, 'mod/addprofit.html')
    
    def post(self, request):

        plan_name = request.POST["plan_name"]
        percentage = request.POST["percentage"]
        days = request.POST["days"]

        plan = models.Plans.objects.get(plan_name=plan_name)
        user_plans = models.User_plan.objects.filter(plan=plan)
        for user_plan in user_plans:

            profit = int(days)*(float(user_plan.invested_amount)*(float(percentage)/100))
            user_plan.user_profit = float(user_plan.user_profit) + profit
            user_plan.save()

            addprofit = models.Addprofit()
            addprofit.user = user_plan.user
            addprofit.plan = plan
            addprofit.profit = profit
            addprofit.percentage = percentage
            addprofit.save()

        return redirect("/moderator/addprofit")
