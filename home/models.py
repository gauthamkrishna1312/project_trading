
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plans(models.Model):

    plan_name = models.CharField(max_length=100)
    plan_price = models.CharField(max_length=100)
    plan_min_percentage = models.CharField(max_length=100)
    plan_max_percentage = models.CharField(max_length=100)
    plan_min_profit = models.CharField(max_length=100)
    plan_max_profit = models.CharField(max_length=100)

class Account_details(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    referral_number = models.CharField(max_length=100)

class User_plan(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    invested_amount = models.CharField(max_length=100)
    plan_status = models.CharField(max_length=100)
    plan_profit = models.CharField(max_length=100)

class Payment(models.Model):

    user_plan = models.ForeignKey(User_plan, on_delete=models.CASCADE)
    transaction_name = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)

class Refarral(models.Model):

    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_referrer")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s_referred")

