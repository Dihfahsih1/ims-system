from django.shortcuts import render, redirect, HttpResponseRedirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import User
from django.views.generic import View
from canonapp.models import *
from django.utils import timezone
from datetime import datetime,timezone
from datetime import datetime as dt
from django.db.models.functions import Length, Upper, datetime
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from accounts.models import Staff

from django.contrib.auth.decorators import login_required



from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from datetime import datetime as dt
from datetime import datetime,timezone
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.db.models import Count, F, Value,Sum
from django.db.models.functions import Length, Upper, datetime

from django.http import HttpResponse

from django.views.generic import View
from django.utils import timezone
from .pdf_render import Render

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import *
from django.shortcuts import redirect, HttpResponseRedirect

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q




from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from accounts.models import Staff




# Create your views here.
@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def executive_home(request):
    return render(request, 'accounts/executive_home.html')

@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/view_profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/view_profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}

        return render(request, 'accounts/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/view_profile')

        else:
            return redirect('/account/change_password')

    else:
        form = PasswordChangeForm(user = request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def login_success(request):

    if request.user.groups.filter(name='Manager'):
        return render(request, 'accounts/home.html')

    elif request.user.groups.filter(name='Executive'):
        return render(request, 'accounts/executive_home.html')

    elif request.user.groups.filter(name='Accountant'):
        return render(request,'accountantapp/Accprofile.html')

    elif request.user.groups.filter(name='Operations'):
        return render(request, 'operationsapp/operations_home.html')

    elif request.user.groups.filter(name='Receptionist'):
        return render(request, 'receptionistapp/receptionist_home.html')

    else:
        return HttpResponseRedirect('Account not found')
        
@login_required        
def executive_driver_payment_archive(request):
    # when we search for monthly archived reports
    if request.method == 'POST':
        report_year = request.POST['report_year'] 
        report_month=request.POST['report_month']
        archived_reports=Driver_payment_Reports_Archive.objects.filter(month=report_month, year=report_year)
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        drivers=Driver.objects.all()
        #getting the current time zone
        today = timezone.now()

        #number of records got
        item_number = archived_reports.count()
    
        # calculating the total balance
        total_bal = archived_reports.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        # calculating the total payments
        total_pai = archived_reports.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
    
        context={'archived_reports':archived_reports,'months':months,'years':years,'drivers':drivers,'driver_total_paid':driver_total_paid,'driver_total_balance':driver_total_balance,'item_number':item_number,
            'today':today,'report_year':report_year,'report_month':report_month
        }
        return render(request,"accounts/executive_driver_payment_archive.html",context)
        

    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accounts/executive_driver_payment_archive.html",context)



########################################################
# printing archived monthly reports
########################################################

class executive_driver_payment_archive_print(View):
   def get(self, request, report_month,report_year):
        archived_reports=Driver_payment_Reports_Archive.objects.filter(month=report_month, year=report_year)
        drivers=Driver.objects.all()
        #getting the current time zone
        today = timezone.now()

        #number of records got
        item_number = archived_reports.count()
    
        # calculating the total balance
        total_bal = archived_reports.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        # calculating the total payments
        total_pai = archived_reports.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
    
        context={'archived_reports':archived_reports,'drivers':drivers,'driver_total_paid':driver_total_paid,'driver_total_balance':driver_total_balance,'item_number':item_number,
            'today':today,'report_year':report_year,'report_month':report_month }

        return Render.render('accounts/executive_driver_payment_archive_print.html', context) 
        
        
        
        
#################################################################
 #Staff Views
################################################################


    #######create staff
@login_required
def staff_create(request):
    if request.method=="POST":
        form=StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_view')
    else:
        form=StaffForm()
        return render(request, 'accounts/staff_create.html', {'form':form})
    

    #################View Staff
@login_required
def staff_view(request):
    items = Staff.objects.all()
    context = {'items': items, }
    return render(request, "accounts/view_staff.html", context)
    

    ###########edit staff
@login_required
def staff_update(request,pk):
    item=get_object_or_404(Staff,pk=pk)

    if request.method=="POST":
        form=StaffForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('staff_view')

    else:
        form=StaffForm(instance=item)
        return render(request, 'accounts/staff_update.html', {'form':form})
    
    
    ###############delete staff
@login_required
def staff_delete(request,pk):
    Staff.objects.filter(id=pk).delete()
    items=Staff.objects.all()
    context={'items':items}
    return render(request, 'accounts/view_staff.html', context)
    


#################################################################
 #Users Views
################################################################


    #######create user
@login_required
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users_view')

    else:
        form = RegistrationForm()
    return render(request, 'accounts/reg_form.html', {'form': form})
    

    #################View users
@login_required
def users_view(request):
    items = User.objects.all()
    context = {'items': items, }
    return render(request, "accounts/users_view.html", context)
    

    ###########edit users
@login_required
def users_edit(request,pk):
    item=get_object_or_404(User,pk=pk)

    if request.method=="POST":
        form=RegistrationForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
        return redirect('users_view')

    else:
        form=RegistrationForm(instance=item)
        return render(request, 'accounts/users_edit.html', {'form':form})
    
    
    ###############delete users
@login_required
def users_delete(request,pk):
    User.objects.filter(id=pk).delete()
    items=User.objects.all()
    context={'items':items}
    return render(request, 'accounts/users_view.html', context)
    
    
    
################################################################################

#########################################
# display_driver_financial statement
##########################################


######################################################
# accountant generate driver financial report
##############################################################
class accountant_generate_driver_financial_report(View):
    @login_required
    def get(self, request, driver_name):
        #first get the driver name
       # driver =Driver.objects.filter(pk=pk).values_list('')

        #driver id to match drivers in payment table
        driver = get_object_or_404(Driver, driver_name=driver_name).id


        #driver name to appear on the report
        driver_name = driver_name


        #passing on the driver attached car
        attached_car=get_object_or_404(Driver, driver_name=driver_name).attached_car

        #Total balance to be paid by driver
        driver_balance=get_object_or_404(Driver, driver_name=driver_name).driver_monthly_payment

        #all payments made by a specific driver
        payments=DriverPayment.objects.filter(driver_name=driver)

        #getting today's date
        today = timezone.now()


        #calculating total paid so far
        total= DriverPayment.objects.filter(driver_name=driver).aggregate(total_amount_paid=models.Sum("paid_amount"))
        total_paid=total["total_amount_paid"]


        #parameters sent to the pdf for display
        params = {
            'attached_car':attached_car,
            'total_paid':total_paid,
            'driver_balance':driver_balance,
            'driver_name':driver_name,
            'request': request,
            'payments': payments,
            'today': today,
        }
        return Render.render('accounts/accountant_driver_financial_report.html', params)


            

######################################
# Searching for archived report
#############################################
@login_required
    
def accountant_driver_payment_archive(request):
    # when we search for monthly archived reports
    if request.method == 'POST':
        report_year = request.POST['report_year'] 
        report_month=request.POST['report_month']
        archived_reports=Driver_payment_Reports_Archive.objects.filter(month=report_month, year=report_year)
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        drivers=Driver.objects.all()
        #getting the current time zone
        today = timezone.now()

        #number of records got
        item_number = archived_reports.count()
    
        # calculating the total balance
        total_bal = archived_reports.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        # calculating the total payments
        total_pai = archived_reports.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
    
        context={'archived_reports':archived_reports,'months':months,'years':years,'drivers':drivers,'driver_total_paid':driver_total_paid,'driver_total_balance':driver_total_balance,'item_number':item_number,
            'today':today,'report_year':report_year,'report_month':report_month
        }
        return render(request,"accounts/accountant_driver_payment_archive.html",context)
        

    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accounts/accountant_driver_payment_archive.html",context)



       ####################################################
      #        CALCULATING TOTALS IN THE REPORTS         #
      ####################################################

def salaryreport(request):
  timezone.now()
  current_month = datetime.datetime.now().month
  queryset = Salary.objects.all().filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accounts/salaryindex.html', context)

# def expenditurereport(request):
def expenditurereport(request):
  current_month = datetime.datetime.now().month
  queryset = Spend.objects.all().filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accounts/expenditureindex.html', context)

# calculating totals in sundryexpense report
def sundryreport(request):
  current_month = datetime.datetime.now().month
  queryset = Sundry.objects.filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accounts/sundryindex.html', context)



   ####################################################
      #        GENERATING REPORTS IN FORM OF PDFS         #
      ####################################################

# Printing Expenditure Report
class expenditurepdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      expense = Spend.objects.filter(Date__month=current_month).order_by('-Date')

      today = timezone.now()
      month = today.strftime('%B')
      totalexpense = 0
      for instance in expense:
          totalexpense += instance.Amount
      expensecontext = {

          'month': month,
          'today': today,
          'expense': expense,
          'request': request,
          'totalexpense': totalexpense,
      }
      return Render.render('accounts/expenditurepdf.html', expensecontext)

# Printing Salaries Report
class salariespdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      salaries = Salary.objects.filter(Date__month=current_month).order_by('-Date')
      today = timezone.now()
      month = today.strftime('%B')
      totalsalary = 0
      for instance in salaries:
          totalsalary += instance.Amount
      salarycontext = {
          'month': month,
          'today': today,
          'salaries': salaries,
          'request': request,
          'totalsalary': totalsalary,
      }
      return Render.render('accounts/pdf.html', salarycontext)

# Printing Sundry Expenses Report
class sundrypdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      sundry = Sundry.objects.filter(Date__month=current_month).order_by('-Date')
      today = timezone.now()
      month = today.strftime('%B')
      totalsundry = 0
      for instance in sundry:
          totalsundry += instance.Amount
      sundrycontext = {
          ''
          'month': month,
          'today': today,
          'sundry': sundry,
          'request': request,
          'totalsundry': totalsundry,
      }
      return Render.render('accounts/sundrypdf.html', sundrycontext)
      
      
      
      

 ##################################
 # This produces the general financial report for all drivers
 ##################################       

def driver_general_financial_report(request):
    
    #when some one submits the financial report
    if request.method == 'POST':
        archived_year = request.POST['archived_year']
        archived_month=request.POST['archived_month']
            
            #getting all the driver_payments
        all_payment_reports=Driver_Payment_Report.objects.all()
        for payment_report in all_payment_reports:
            driver_name=payment_report.driver_name
            driver_car=payment_report.driver_car
            balance=payment_report.balance
            amount_paid=payment_report.amount_paid
            date=payment_report.date
    
            #getting the archives object to creation
            payment_report_archive_object=Driver_payment_Reports_Archive()
    
            payment_report_archive_object.driver_name=driver_name
            payment_report_archive_object.amount_paid=amount_paid
            payment_report_archive_object.driver_car=driver_car
            payment_report_archive_object.balance=balance
            payment_report_archive_object.date=date
            payment_report_archive_object.month=archived_month
            payment_report_archive_object.year=archived_year


            #getting the specific driver object and updating its current balance
            Driver.objects.filter(driver_name=driver_name).update(
                driver_monthly_payment=F('driver_monthly_payment_ref')+balance
            )
    
            payment_report_archive_object.save()
    
        #This deletes all the current report data after creation of a monthly archive.
        all_payment_reports.delete()
    
        #retrieving all the payment receipts
        driver_receipts=DriverPayment.objects.all()
        for receipt in driver_receipts:
            date=receipt.date
            driver_name=receipt.driver_name
            paid_amount=receipt.paid_amount
            paid_by=receipt.paid_by
            received_by=receipt.received_by
    
            #get the receipt archive object
            payment_receipt_archive=DriverPayments_Archive()
            payment_receipt_archive.date=date
            payment_receipt_archive.driver_name=driver_name
            payment_receipt_archive.paid_amount=paid_amount
            payment_receipt_archive.paid_by=paid_by
            payment_receipt_archive.received_by=received_by
            payment_receipt_archive.month=archived_month
            payment_receipt_archive.year=archived_year
            
            payment_receipt_archive.save()
        #this deletes all the previous driver receipts
        driver_receipts.delete()
        
        message="You have successfully archived the payment report and all payment receipts for "+archived_month+" "+archived_year
        all_drivers = Driver.objects.all()
        #loop through all drivers available
        for driver in all_drivers:
    
            driver_name=driver.driver_name
            driver_id=driver.id
            driver_car=driver.attached_car
            driver_balance=driver.driver_monthly_payment
    
            # calculating total paid so far
            total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(total_amount_paid=models.Sum("paid_amount"))
            total_paid = total["total_amount_paid"]
            report_item=Driver_Payment_Report()
            report_item.driver_name=driver_name
            report_item.amount_paid=total_paid
            report_item.balance=driver_balance
            report_item.driver_car=driver_car
    
            # first check for availability of an object(filtering)
            if Driver_Payment_Report.objects.filter(driver_name=driver_name):
                Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,balance=driver_balance)
    
            else:
             report_item.save()
    
        items=Driver_Payment_Report.objects.all()
        item_number=items.count()
    
        #calculating the total balance
        total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        #calculating the total payments
        total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
        
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                    'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        
        context={'message':message,
        'months':months,
        'years':years,
        'driver_total_balance':driver_total_balance,
        'driver_total_paid':driver_total_paid,
        'items':items,
        'item_number':item_number
        }
    
        return  render(request, "accounts/driver_general_financial_report.html",context)
    
    #the if for post data  of archiving ends here
    
    all_drivers = Driver.objects.all()
    #loop through all drivers available
    for driver in all_drivers:

        driver_name=driver.driver_name
        driver_id=driver.id
        driver_car=driver.attached_car
        driver_balance=driver.driver_monthly_payment
        driver_payment_ref=driver.driver_monthly_payment_ref

        # calculating total paid so far
        total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(total_amount_paid=models.Sum("paid_amount"))
        total_paid = total["total_amount_paid"]
        
        #Driver.objects.filter()
        
        
        
        #report item variables
        report_item=Driver_Payment_Report()
        report_item.driver_name=driver_name
        report_item.amount_paid=total_paid
        report_item.balance=driver_balance
        report_item.driver_car=driver_car

        # first check for availability of an object(filtering)
        if Driver_Payment_Report.objects.filter(driver_name=driver_name):
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,balance=driver_balance)

        else:
         report_item.save()

    items=Driver_Payment_Report.objects.all()
    item_number=items.count()

    #calculating the total balance
    total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
    driver_total_balance = total_bal["total_bal"]

    #calculating the total payments
    total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
    driver_total_paid = total_pai["total_pai"]
    
    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]


    context={
        'months':months,
        'years':years,
        'driver_total_balance':driver_total_balance,
        'driver_total_paid':driver_total_paid,
        'items':items,
        'item_number':item_number
    }

    return render(request, "acounts/driver_general_financial_report.html",context)

##########################################################
# printing of the general financial report
####################################################

class print_general_financial_report(View):

    def get(self, request):
        today = timezone.now()

        items = Driver_Payment_Report.objects.all()
        item_number = items.count()

        # calculating the total balance
        total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]

        # calculating the total payments
        total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]

        params = {
        'driver_total_balance':driver_total_balance,
        'driver_total_paid':driver_total_paid,
        'items':items,
        'item_number':item_number,
        'today': today,
        }
        return Render.render('accounts/print_general_financial_report.html', params)
        
        
        ###############################################################################################
        # searching for the archives
def executive_expensesarchivessearch(request):
    if request.method == 'POST':
        report_year = request.POST['report_year']
        report_month = request.POST['report_month']
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'August', 'September', 'October', 'November','December']
        years = [2019, 2020]
        today = timezone.now()
        archived_reports = ExpensesReportArchive.objects.filter(month=report_month, year=report_year)
        total = archived_reports.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]


        context = {'archived_reports':archived_reports,
                   'months': months,
                   'years': years,
                   'total_amount': total_amount,
                   'today': today,
                   'report_year': report_year,
                   'report_month': report_month
                   }
        return render(request, "accounts/expenditurearchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October', 'November', 'November', 'December']
    years = [2019, 2020]
    expenses=ExpensesReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'expenses': expenses}
    return render(request, "accounts/expenditurearchive.html", context)


def executive_salaryarchivessearch(request):
    if request.method == 'POST':
        report_year = request.POST['report_year']
        report_month = request.POST['report_month']
        archived_reports = SalaryReportArchive.objects.filter(archivedmonth=report_month, archivedyear=report_year)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'August', 'September', 'October',  'November','December']
        years = [2019, 2020]

        salary = SalaryReportArchive.objects.all()
        today = timezone.now()
        total = archived_reports.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]

        context = {'archived_reports': archived_reports,
                   'months': months,
                   'years': years,
                   'expenses':salary,
                   'total_amount': total_amount,
                   'today': today,
                   'report_year': report_year,
                   'report_month': report_month
                   }
        return render(request, "accounts/salaryarchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October',  'November', 'December']
    years = [2019, 2020]

    salary=SalaryReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'salary': salary}
    return render(request, "accounts/salaryarchive.html", context)

def executive_sundryarchivessearch(request):
    if request.method == 'POST':
        report_year = request.POST['report_year']
        report_month = request.POST['report_month']
        archived_reports = SundryReportArchive.objects.filter(month=report_month, year=report_year)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'August', 'September', 'October', 'November','December']
        years = [2019, 2020]

        sundry = SundryReportArchive.objects.all()
        today = timezone.now()
        total = archived_reports.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]

        context = {'archived_reports': archived_reports,
                   'months': months,
                   'years': years,
                   'expenses':sundry,
                   'total_amount': total_amount,
                   'today': today,
                   'report_year': report_year,
                   'report_month': report_month
                   }
        return render(request, "accounts/sundryarchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October', 'November', 'November', 'December']
    years = [2019, 2020]

    sundry=SundryReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'sundry': sundry}
    return render(request, "accounts/sundryarchive.html", context)
    

   ####################################################
    #        GENERATING REPORTS IN FORM OF ANNUAL PDFS #
    ####################################################

# Printing Expenditure archived Report
class executive_expenditurearchivepdf(View):
    def get(self, request, report_month, report_year):
        archived_expenses = ExpensesReportArchive.objects.filter(month=report_month, year=report_year)
        today = timezone.now()
        month = today.strftime('%B')
        total = archived_expenses.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]
        expensecontext = {
            'today': today,
            'total_amount': total_amount,
            'request': request,
            'archived_expenses': archived_expenses,
            'report_year': report_year,
            'report_month': report_month
        }
        return Render.render('accounts/expenditurearchivepdf.html', expensecontext)


# Printing Salaries archived Report
class executive_salaryarchivepdf(View):
    def get(self, request, report_month, report_year):
        archived_salary = SalaryReportArchive.objects.filter(archivedmonth=report_month, archivedyear=report_year)
        today = timezone.now()
        total = archived_salary.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]
        salarycontext = {
            'today': today,
            'total_amount': total_amount,
            'request': request,
            'archived_salary': archived_salary,
        }
        return Render.render('accounts/salaryarchivepdf.html', salarycontext)


# Printing Sundry Expenses archived Report
class executive_sundryarchivepdf(View):
    def get(self, request, report_month, report_year):
        archived_sundry = SundryReportArchive.objects.filter(month=report_month, year=report_year)
        today = timezone.now()
        month = today.strftime('%B')
        total = archived_sundry.aggregate(totals=models.Sum("Amount"))
        total_amount = total["totals"]
        sundrycontext = {
            'today': today,
            'total_amount': total_amount,
            'request': request,
            'archived_sundry': archived_sundry,
        }
        return Render.render('accounts/sundryarchivepdf.html', sundrycontext)


  ####################################################
  #        ARCHIVING OF THE MONTHLY REPORTS          #
  ####################################################
@login_required
def executive_salaryarchive(request):
    salaryarchived = SalaryReportArchive.objects.all().order_by('-Date')
    total = SalaryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'salaryarchived': salaryarchived
               }
    return render(request, 'accounts/salaryarchive.html', context)

@login_required
def executive_expenditurearchive(request):
    expensesarchived = ExpensesReportArchive.objects.all().order_by('-Date')
    total = SalaryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'expensesarchived':expensesarchived
    }
    return render(request, 'accounts/expenditurearchive.html', context)

# calculating totals in sundryexpense report
@login_required
def executive_sundryarchive(request):
    sundryarchived = SundryReportArchive.objects.all().order_by('-Date')
    total = SundryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'sundryarchived': sundryarchived
               }
    return render(request, 'accounts/sundryarchive.html', context)


        
