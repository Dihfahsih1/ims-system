from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetCompleteView
from django.conf.urls import url
from .import views
from accounts import views



urlpatterns = [
    path('', home, name='home'),

    path('executive_home/',executive_home, name='executive_home'),
    
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    path('view_profile/', view_profile, name='view_profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    
    path('login_success/', login_success, name='login_success'),

    path('change_password', change_password, name='change_password'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name='reset_password'),

    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), {'template_name':'accounts/reset_password_done.html'}, name='reset_password_done'),
    path('reset_password_confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='reset_password_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='reset_password_complete'),



    path('executive_driver_payment_archive/', executive_driver_payment_archive, name="executive_driver_payment_archive"),
    url(r'^executive_driver_payment_archive_print/(?P<report_month>.+?)/(?P<report_year>.+?)$', executive_driver_payment_archive_print.as_view(), name="executive_driver_payment_archive_print"),
    
    
    
    url(r'^driver_general_financial_report$', driver_general_financial_report, name="driver_general_financial_report"),

    
    
    
    #DISPLAYING CURRENT MONTHL REPORT
    url(r'^sundryreport', sundryreport ,name='sundryreport'),
    url(r'^salaryreport/', salaryreport, name='salaryreport'),
    url(r'^expenditurereport/', expenditurereport, name='expenditurereport'),

    #PRINTING MONTHLY REPORTS
    url(r'^salariespdf/', salariespdf.as_view() ,name='salariespdf'),
    url(r'^sundrypdf/', sundrypdf.as_view() ,name='sundrypdf'),
    url(r'^expenditurepdf/', expenditurepdf.as_view() ,name='expenditurepdf'),
    
    
    
##########################################################################################
    

    url(r'^staff_new', staff_create, name="staff_new"),
    url(r'^staff_view$', staff_view, name="staff_view"),
    url(r'^staff_delete/(?P<pk>\d+)$', staff_delete, name="staff_delete"),
    url(r'^staff_update/(?P<pk>\d+)$', staff_update, name="staff_update"),
    
    
    path('register/', register, name='register'),
    url(r'^users_view', users_view, name="users_view"),
    url(r'^users_delete/(?P<pk>\d+)$', users_delete, name="users_delete"),
    url(r'^users_edit/(?P<pk>\d+)$', users_edit, name="users_edit"),
    
    
######################################################################################
#DISPLAYING MONTHLY ARCHIVED REPORTS
    url(r'^executive_expenditurearchive/', executive_expenditurearchive, name='executive_expenditurearchive'),
    url(r'^executive_salaryarchive/', executive_salaryarchive, name='executive_salaryarchive'),
    url(r'^executive_sundryarchive/', executive_sundryarchive, name='executive_sundryarchive'),
 
    #PRINTING GENERAL MONTHLY ARCHIVED REPORTS
    url(r'^executive_expenditurearchivepdf/(?P<report_month>.+?)/(?P<report_year>.+?)/',executive_expenditurearchivepdf.as_view(), name='executive_expenditurearchivepdf'),
    url(r'^executive_salaryarchivepdf/(?P<report_month>.+?)/(?P<report_year>.+?)/',executive_salaryarchivepdf.as_view(), name='executive_salaryarchivepdf'),
    url(r'^executive_sundryarchivepdf/(?P<report_month>.+?)/(?P<report_year>.+?)/',executive_sundryarchivepdf.as_view(), name='executive_sundryarchivepdf'),
    
    #SEARCHING FOR THE ARCHIVED DATA
    url(r'^executive_expensesarchivessearch/', executive_expensesarchivessearch, name='executive_expensesarchivessearch'),
    url(r'^executive_salaryarchivessearch/', executive_salaryarchivessearch, name='executive_salaryarchivessearch'),
    url(r'^executive_sundrysarchivessearch/',executive_sundryarchivessearch, name='executive_sundryarchivessearch'),
]