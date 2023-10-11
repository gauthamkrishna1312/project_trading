from django.urls import path, include
from . import views

urlpatterns = [   
    path('', views.Index_view.as_view(), name='home'),
    path('contact/', views.Contact_view.as_view(), name='contact'),
    path('yourplan/', views.Yourplan_view.as_view(), name='yourplan'),
    path('newplan/', views.Newplan_view.as_view(), name='newplan'),
    path('profit/', views.Profit_view.as_view(), name='profit'),
    path('withdraw/', views.Withdraw_view.as_view(), name='withdraw'),
    path('refer/', views.Refer_view.as_view(), name='refer'),
    path('payment/', views.Payment_view.as_view(), name='payment'),
    path('profile/', views.Profile_view.as_view(), name='profile'),
    path('history/', views.History_view.as_view(), name='history'),
    path('admindex/', views.Admindex_view.as_view(), name='admindex'),
    path('admreg/', views.Admreg_view.as_view(), name='admreg'),
    path('admregact/', views.Admregact_view.as_view(), name='admregact'),
    path('admpayments/', views.Admpayments_view.as_view(), name='admpayments'),
    path('admwithdraw/', views.Admwithdraw_view.as_view(), name='admwithdraw'),
    path('admaddprofit/', views.Admaddprofit_view.as_view(), name='admaddprofit'),
    path('admaddplan/', views.Admaddplan_view.as_view(), name='admaddplan'),
    path('admeditplan/', views.Admeditplan_view.as_view(), name='admeditplan'),
    path('signup/', views.Signup_view.as_view(), name='signup'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', views.Logout_view.as_view(), name='logout'),
]