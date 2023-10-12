from django.urls import path, include
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [   
    path('', login_required(views.Index_view.as_view()), name='home'),
    path('contact/', login_required(views.Contact_view.as_view()), name='contact'),
    path('yourplan/', login_required(views.Yourplan_view.as_view()), name='yourplan'),
    path('newplan/', login_required(views.Newplan_view.as_view()), name='newplan'),
    path('profit/', login_required(views.Profit_view.as_view()), name='profit'),
    path('withdraw/', login_required(views.Withdraw_view.as_view()), name='withdraw'),
    path('refer/', login_required(views.Refer_view.as_view()), name='refer'),
    path('payment/', login_required(views.Payment_view.as_view()), name='payment'),
    path('profile/', login_required(views.Profile_view.as_view()), name='profile'),
    path('history/', login_required(views.History_view.as_view()), name='history'),
    path('moderator/index/', login_required(views.Admindex_view.as_view()), name='adm_index'),
    path('moderator/members/', login_required(views.Admreg_view.as_view()), name='adm_mambers'),
    path('moderator/activemembers/', login_required(views.Admregact_view.as_view()), name='adm_active_member'),
    path('moderator/payments/', login_required(views.Admpayments_view.as_view()), name='adm_payments'),
    path('moderator/withdraw/', login_required(views.Admwithdraw_view.as_view()), name='adm_withdraw'),
    path('moderator/addprofit/', login_required(views.Admaddprofit_view.as_view()), name='adm_add_profit'),
    path('moderator/addplan/', login_required(views.Admaddplan_view.as_view()), name='adm_add_plan'),
    path('moderator/editplan/', login_required(views.Admeditplan_view.as_view()), name='adm_edit_plan'),
    path('editplan/<int:plan_id>', login_required(views.Editplan_view.as_view()), name='edit_plan'),
    path('signup/', views.Signup_view.as_view(), name='signup'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', login_required(views.Logout_view.as_view()), name='logout'),
]