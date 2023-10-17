from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from random import randint

from . import models


class Index_view(View):

    def get(self, request):

        if request.user.is_superuser:
                return redirect("/moderator/dashboard/")
        
        return redirect("/dashboard")

class Dashboard_view(View):
    
    def get(self, request):
        
        user_plans = models.User_plan.objects.filter(user=request.user)
        payments = [payment for payment in models.Payment.objects.filter(user=request.user) if payment.transaction_status != "approved"]
        withdraws = [withdraw for withdraw in models.Withdraw.objects.filter(user=request.user) if withdraw.withdraw_status != "done"]

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
        referral_id = request.POST.get("referral_id", None)

        temp_context = {
                "fname": fname,
                "lname": lname,
                "email": email,
                "uname": uname,
                "referral": referral_id,
            }
        
        if models.User.objects.filter(email=email).exists() == True:

            messages.error(request, f"an account exists in this email {email}")
            return redirect("/signup")
        
        if models.User.objects.filter(username=uname).exists() == True:

            messages.error(request, "username is taken")
            return redirect("/signup")
        
        if models.User.objects.filter(username=uname, email=email).exists() == True:

            messages.error(request, "user already exists")
            return redirect("/signup")
        
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

        print("user created")

        self.add_user_plan(request.user)
        print("user_plan added")
        self.add_referral(request.user)
        print("referral added")
        print(f"refer [{referral_id}]")
        if len(referral_id) > 5:
            self.add_referred(request.user, referral_id)
            print("referral tree")

        messages.success(request, "Signup Successful")
        return redirect("/dashboard")
    
    def add_user_plan(self, user):

        user_plan = models.User_plan()
        user_plan.user = user
        user_plan.invested_amount = "0"
        user_plan.plan = models.Plans.objects.get(id=1)
        user_plan.user_status = "Inactive"
        user_plan.user_profit = "0"
        user_plan.user_referral_profit = "0"
        user_plan.save()

    def add_referral(self, user):

        referral = models.Referral()
        referral.user = user
        referral.referral_details = models.ReferralDetails.objects.all()[0]
        referral_id = str(user.username)+"@"+str(randint(1000, 9999))
        referral.referral_id = referral_id
        referral.save()

    def add_referred(self, user, id):

        referred_user = models.Referral.objects.get(referral_id=id)
        referred_user.direct.add(user)
        referred_user.save()
        
        referrer_user = models.Referral.objects.get(user=user)
        referrer_user.referred_user = referred_user.user
        referrer_user.save()

        if referred_user.referred_user is not None:
            referred_user_1 = models.Referral.objects.get(user=referred_user.referred_user)
            referred_user_1.level_1.add(referrer_user.user)
            if referred_user_1.referred_user is not None:
                referred_user_2 = models.Referral.objects.get(user=referred_user_1.referred_user)
                referred_user_2.level_2.add(referrer_user.user)
                if referred_user_2.referred_user is not None:
                    referred_user_3 = models.Referral.objects.get(user=referred_user_2.referred_user)
                    referred_user_3.level_3.add(referrer_user.user)


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

        if float(withdraw_amount) < 10:

            messages.info(request, "minimum amount is 10")
            return redirect("/withdraw")

        user_plan = models.User_plan.objects.get(user=request.user)

        if float(withdraw_amount) > float(user_plan.user_profit):

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

        context = {
            "refer": models.Referral.objects.get(user=request.user),
            "members": models.Referral.objects.get(user=request.user).direct.all(),
        }

        return render(request, 'user/refer.html', context=context)

class Payment_view(View):
    
    def get(self,request):

        return render(request, 'user/payment.html')
    
    def post(self, request):
        
        transaction_name = request.POST["transaction_name"]
        transaction_id = request.POST["transaction_id"]
        amount = request.POST["amount"]

        
        if float(amount) < 100:
            messages.info(request, "minimum amount is 100")
            return render(request, "user/payment.html")
        if float(str(float(amount)/50).split(".")[1]) > 0:
            messages.info(request, "only multiples of 50")
            return render(request, "user/payment.html")
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

        if request.user.is_superuser:
            
            user = models.User.objects.get(id=kwargs['id'])
            context = {
                "payments": models.Payment.objects.filter(user=user),
                "withdraws":  models.Withdraw.objects.filter(user=user),
                "addprofits": models.Addprofit.objects.filter(user=user),
                "action": action,
                "user": user,
                "admin": True,
            }

            return render(request, "mod/history.html", context=context)

        context = {
            "payments": models.Payment.objects.filter(user=request.user),
            "withdraws": models.Withdraw.objects.filter(user=request.user),
            "addprofits": models.Addprofit.objects.filter(user=request.user),
            "action": action,
        }

        return render(request, 'user/history.html', context=context)




class ModDashboard_view(View):
    
    def get(self,request):
        return render(request, 'mod/index.html')

class ModMembers_view(View):
    
    def get(self, request, **kwargs):

        if "status" in kwargs:
            
            context = {
                "members": [[member, referred] for member in models.User_plan.objects.filter(user_status=kwargs["status"]) for referred in models.Referral.objects.filter(user=member.user)],
            }

            return render(request, 'mod/membersactive.html', context=context)

        context = {
            "members": [ [user, referred, user_plan] for user in User.objects.all() if not user.is_superuser for referred in models.Referral.objects.filter(user=user) for user_plan in models.User_plan.objects.filter(user=user)],
        }

        return render(request, 'mod/members.html', context=context)


class ModPayments_view(View):
    
    def get(self,request, **kwargs):

        action = kwargs["action"]
        
        if "id" in kwargs:
            
            payment_id = kwargs["id"]

            payment = models.Payment.objects.get(id=payment_id)
            if action == "approve":
                if payment.transaction_status == "Approved":
                    
                    messages.error(request, "already approved")
                    return redirect("/moderator/payments/approved")
                
                if models.User_plan.objects.filter(user=payment.user).exists() == True:

                    user_plan = models.User_plan.objects.get(user=payment.user)
                    user_plan.invested_amount = str(float(user_plan.invested_amount) + float(payment.transaction_amount))
                    plan = self.get_plan(user_plan.invested_amount)
                    user_plan.plan = plan
                    user_plan.user_status = "Active"
                    if not user_plan.user.is_active:
                        user_plan.user.is_active = True
                    user_plan.save()


                payment.transaction_status = "approved"
                payment.save()

                messages.success(request, "payment approved")
                return redirect("/moderator/payments/approved")

            elif action == "reject":

                payment.transaction_status = 'rejected'
                payment.save()

                messages.success(request, "payment rejected")
                return redirect("/moderator/payments/rejected")

        
        context = {
            "payments": models.Payment.objects.filter(transaction_status=action),
            "action": action,
        }

        return render(request, "mod/payments.html", context=context)
        
    def get_plan(self, amount):

        plan_db = models.Plans.objects.all()
        for plan in plan_db:
            if float(amount) >= float(plan.plan_min_price) and float(amount) < float(plan.plan_max_price):
                return plan

class ModWithdraw_view(View):
    
    def get(self,request, **kwargs):

        if "id" in kwargs:

            withdraw_id = kwargs["id"]
            action = kwargs["action"]

            withdraw = models.Withdraw.objects.get(id=withdraw_id)

            if action == "done":
                
                user_plan = models.User_plan.objects.get(user=withdraw.user)
                user_plan.user_profit = str(float(user_plan.user_profit) - float(withdraw.withdraw_amount))
                user_plan.save()
                withdraw.withdraw_status = "done"
                withdraw.save()

                messages.success(request, "withdraw success")
                return redirect("/moderator/withdraw/done")
            
            elif action == "rejected":

                withdraw.withdraw_status = "rejected"
                withdraw.save()

                messages.success(request, "withdraw rejected")
                return redirect("/moderator/withdraw/rejected")

        status = kwargs["status"]
        context = {
            "withdraws": models.Withdraw.objects.filter(withdraw_status=status),
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
            if float(amount) >= float(plan.plan_min_price) and float(amount) < float(plan.plan_max_price):
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

        context = {
            "plans": models.Plans.objects.all(),
            "members": [member for member in models.User.objects.all() if not member.is_superuser]
        }

        return render(request, 'mod/addprofit.html', context=context)
    
    def post(self, request):

        plan_name = request.POST.get("plan_name", None)
        percentage = request.POST.get("percentage", None)

        uname = request.POST.get("uname", None)
        amount = request.POST.get("amount", None)

        days = request.POST["days"]\
        
        if uname == None:

            plan = models.Plans.objects.get(plan_name=plan_name)
            user_plans = models.User_plan.objects.filter(plan=plan)
            for user_plan in user_plans:

                profit = float(days)*(float(user_plan.invested_amount)*(float(percentage)/100))
                user_plan.user_profit = float(user_plan.user_profit) + profit
                user_plan.days = float(user_plan.days) + float(days)

                self.add_referral_profit(user_plan.user, amount)
                
                user_plan.total_profit = str(float(user_plan.user_profit) + float(user_plan.user_referral_profit))
                user_plan.save()

                addprofit = models.Addprofit()
                addprofit.user = user_plan.user
                addprofit.plan = plan
                addprofit.profit = profit
                addprofit.percentage = percentage
                addprofit.save()

        else:

            user = models.User.objects.get(username=uname)
            user_plan = models.User_plan.objects.get(user=user)
            user_plan.user_profit = float(user_plan.user_profit) + float(amount)
            user_plan.days = float(user_plan.days) + float(days)

            self.add_referral_profit(user, amount)

            user_plan.total_profit = str(float(user_plan.user_profit) + float(user_plan.user_referral_profit))
            user_plan.save()

            addprofit = models.Addprofit()
            addprofit.user = user
            addprofit.plan = user_plan.plan
            addprofit.profit = amount
            addprofit.save()

        messages.success(request, "profit added")
        return redirect("/moderator/addprofit")
    
    def add_referral_profit(self, user, amount):

        referral = models.Referral.objects.get(user=user)
        if referral.referred_user is not None:
            referral_1 = models.Referral.objects.get(user=referral.referred_user)
            user_plan = models.User_plan.objects.get(user=referral.referred_user)
            user_plan.user_referral_profit = float(user_plan.user_referral_profit) + (float(amount)*(float(referral_1.referral_details.percent_direct)/100))
            user_plan.save()
            if referral_1.referred_user is not None:
                referral_2 = models.Referral.objects.get(user=referral_1.referred_user)
                user_plan = models.User_plan.objects.get(user=referral_1.referred_user)
                user_plan.user_referral_profit = float(user_plan.user_referral_profit) + (float(amount)*(float(referral_2.referral_details.percent_level_1)/100))
                user_plan.save()
                if referral_2.referred_user is not None:
                    referral_3 = models.Referral.objects.get(user=referral_2.referred_user)
                    user_plan = models.User_plan.objects.get(user=referral_2.referred_user)
                    user_plan.user_referral_profit = float(user_plan.user_referral_profit) + (float(amount)*(float(referral_3.referral_details.percent_level_2)/100))
                    user_plan.save()
                    if referral_3.referred_user is not None:
                        referral_4 = models.Referral.objects.get(user=referral_3.referred_user)
                        user_plan = models.User_plan.objects.get(user=referral_3.referred_user)
                        user_plan.user_referral_profit = float(user_plan.user_referral_profit) + (float(amount)*(float(referral_3.referral_details.percent_level_3)/100))
                        user_plan.save()

