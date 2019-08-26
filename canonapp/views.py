from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from  accounts import models
from accounts.forms import StaffForm

from .forms import *
from datetime import datetime as dt
from datetime import datetime,timezone
from .resources import *
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.db.models import Count, F, Value,Sum
from django.db.models.functions import Length, Upper, datetime

from django.http import HttpResponse
import requests

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
from  accounts.models import *



IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# Create your views here.

#########################
# operations manager viewing cars
###########################

def operations_view_cars(request):
    items = Car.objects.all()
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_cars.html", context)

#################################
# receptionist viewing cars
#################################

def receptionist_view_cars(request):
    items = Car.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_cars.html", context)

################################
# operations manager adding car
#############################

def operations_add_car(request):
    if request.method=="POST":
        form=CarForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('operations_view_cars')
    else:
        form=CarForm()
        return render(request, 'operationsapp/operations_add_car.html', {'form':form})

##########################
#  Receptionist_home page
#########################
def receptionist_home(request):


    return render(request,"receptionistapp/receptionist_home.html")

##############################
# operations delete car
##############################

def operations_delete_car(request,pk):
    Car.objects.filter(id=pk).delete()
    items=Car.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_cars.html', context)

########################################
# Receptionist add complaint
###############################################


def receptionist_add_complaint(request):
    if request.method=="POST":
        form=ComplaintsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist_view_complaints')
    else:
        form=ComplaintsForm()
        return render(request, 'receptionistapp/receptionist_add_complaint.html', {'form':form})
        
############################################
# operations add driver
#########################################
def operations_add_driver(request):
    if request.method=="POST":
        form=DriverForm(request.POST,request.FILES)
        if form.is_valid():

            car = get_object_or_404(Car, car_registration_no=form.cleaned_data['attached_car'].car_registration_no)

            if car.availability=='TAKEN':
                info='The selected car has already been assigned to a driver'
                form = DriverForm()
                return render(request,'operationsapp/operations_add_driver.html',{'info':info,'form':form})

            else:

                # updating the car status
                Car.objects.filter(car_registration_no=form.cleaned_data['attached_car'].car_registration_no) \
                    .update(availability='TAKEN')

                form.save()

                info='The driver successfully registered'
                items = Driver.objects.all()

                return render(request,'operationsapp/operations_view_drivers.html',{'info':info,'items': items})
    else:
        form=DriverForm()
        return render(request, 'operationsapp/operations_add_driver.html', {'form':form})

###########################################
# receptionist view complaints
####################################################
def receptionist_view_complaints(request):
    items = Complaints.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_complaints.html", context)

############################################
# receptionist view drivers
##################################################
def receptionist_view_drivers(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_drivers.html", context)
#############################################
# operations view drivers
###################################################
def operations_view_drivers(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_drivers.html", context)
#############################################
# operations edit car
#############################################
def operations_edit_car(request,pk):
    item=get_object_or_404(Car,pk=pk)

    if request.method=="POST":
        form=CarForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('operations_view_cars')

    else:
        form=CarForm(instance=item)
        return render(request, 'operationsapp/operations_edit_car.html', {'form':form})
############################################
# receptionist edit complaint
#####################################################
def receptionist_edit_complaint(request,pk):
    item=get_object_or_404(Complaints,pk=pk)
    if request.method=="POST":
        form=ComplaintsForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('receptionist_view_complaints')
    else:
        form=ComplaintsForm(instance=item)
    return render(request, 'receptionistapp/receptionist_edit_complaint.html', {'form':form})
####################################################
# operations edit driver
#######################################################
def operations_edit_driver(request,pk):
    item=get_object_or_404(Driver,pk=pk)
    
    #updating all related instances
    driver_name=item.driver_name

    if request.method=="POST":
        form=DriverForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(driver_name=form.cleaned_data['driver_name'])
            form.save()
            return redirect('operations_view_drivers')

    else:
        form=DriverForm(instance=item)
        return render(request, 'operationsapp/operations_edit_driver.html', {'form':form})
    
    
##############################################
# operations delete car
#################################################
def operations_delete_car(request,pk):
    Car.objects.filter(id=pk).delete()
    items=Car.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_cars.html', context)
    
    
#############################################
# receptionist delete complaint
#######################################################
def receptionist_delete_complaint(request,pk):
    Complaints.objects.filter(id=pk).delete()
    items=Complaints.objects.all()
    context={'items':items}
    return render(request, 'receptionistapp/receptionist_view_complaints.html', context)
    
    
##################################################
# operations delete driver
########################################################
def operations_delete_driver(request,pk):
    driver=Driver.objects.filter(id=pk)
    #search for all driver associated data
    #DriverPayment.objects.filter(driver_name=driver.id).delete()
    #Driver_Payment_Report.objects.filter(driver_name=driver.driver_name).delete()
    #DriverPayments_Archive.objects.filter(driver_name=driver.id).delete()
    #Driver_payment_Reports_Archive.objects.filter(driver_name=driver.driver_name).delete()
    
    #get associated car to the driver 
    car_id=Driver.objects.filter(id=pk).attached_car
    
    #update the car to availability
    Car.objects.filter(id=car_id).update(availability='AVAILABLE')
    
    #delete driver object
    driver.delete()
    items=Driver.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_drivers.html', context)
    
    
################################################
# receptionist forward complaint
###################################################
def receptionist_forward_complaint(request,pk):
    complaint=Complaints.objects.filter(id=pk)
    complaint.update(forwarded_status='FORWARDED')
    items=Complaints.objects.all()
    context={'items':items}
    return render(request, 'receptionistapp/receptionist_view_complaints.html', context)


###############################################
# operations home
####################################################
def operations_home(request):
    return render(request, 'operationsapp/operations_home.html')

###############################################
# operations view complaints
#####################################################
def operations_view_complaints(request):
    items = Complaints.objects.filter(forwarded_status='FORWARDED')
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_complaints.html", context)


#################################################
# operations export cars
####################################################
def operations_export_cars(request):
    car_resource = CarResource()
    dataset = car_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cars.csv"'
    return response

###################################################
# operations export driver data
#####################################################

def operations_export_drivers(request):
    driver_resource = DriverResource()
    dataset = driver_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="drivers.csv"'
    return response

################################################
# operations view driver payments
#########################################################


def operations_view_driver_payments(request):
    
        # when sending SMS to a driver
    if request.method == 'POST':
        message = request.POST['sms_message']
        driv_name=request.POST['driver_name']
        contact=get_object_or_404(Driver,driver_name=driv_name).driver_contact

        # Your Account Sid and Auth Token from twilio.com/console
        custome_message="CANON INNOVATIONS LTD,\n"+"Dear "+driv_name+",\n"+message
        
        message_number=contact.lstrip("0")
        
        
        #SENDING MESSAGES
        
        post_data={'user':'canon','password':'mediat*45TYZ','sender':'CANON','message':custome_message,'reciever':'256'+message_number}
        
        post_response=requests.post(url='http://boxuganda.com/api.php',data=post_data)
        
        sms_balance=requests.get(url='http://boxuganda.com/balance.php?user=canon&password=mediat*45TYZ')
        
        message2="You have successfully sent a message to "+driv_name+","+"  Your SMS balance is:"+sms_balance.text+"SMS's"
        
        
        
        #getting all the driver info back
        all_drivers = Driver.objects.all()
        # loop through all drivers available
        for driver in all_drivers:
    
            driver_name = driver.driver_name
            driver_id = driver.id
            driver_car = driver.attached_car
            driver_balance = driver.driver_monthly_payment
    
            # calculating total paid so far
            total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(
                total_amount_paid=models.Sum("paid_amount"))
            total_paid = total["total_amount_paid"]
            report_item = Driver_Payment_Report()
            report_item.driver_name = driver_name
            report_item.amount_paid = total_paid
            report_item.balance = driver_balance
            report_item.driver_car = driver_car
    
            # first check for availability of an object(filtering)
            if Driver_Payment_Report.objects.filter(driver_name=driver_name):
                Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,
                                                                                     balance=driver_balance)
    
            else:
                report_item.save()
    
        items = Driver_Payment_Report.objects.all()
        item_number = items.count()
    
        # calculating the total balance
        total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        # calculating the total payments
        total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
       
        context={'message':message2,
        'driver_total_balance': driver_total_balance,
        'driver_total_paid': driver_total_paid,
        'items': items,
        'item_number': item_number
        }

        return render(request,'operationsapp/operations_view_driver_payments.html',context)

    all_drivers = Driver.objects.all()
    # loop through all drivers available
    for driver in all_drivers:

        driver_name = driver.driver_name
        driver_id = driver.id
        driver_car = driver.attached_car
        driver_balance = driver.driver_monthly_payment

        # calculating total paid so far
        total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(
            total_amount_paid=models.Sum("paid_amount"))
        total_paid = total["total_amount_paid"]
        report_item = Driver_Payment_Report()
        report_item.driver_name = driver_name
        report_item.amount_paid = total_paid
        report_item.balance = driver_balance
        report_item.driver_car = driver_car

        # first check for availability of an object(filtering)
        if Driver_Payment_Report.objects.filter(driver_name=driver_name):
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,
                                                                                 balance=driver_balance)

        else:
            report_item.save()

    items = Driver_Payment_Report.objects.all()
    item_number = items.count()

    # calculating the total balance
    total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
    driver_total_balance = total_bal["total_bal"]

    # calculating the total payments
    total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
    driver_total_paid = total_pai["total_pai"]




    context = {
        'driver_total_balance': driver_total_balance,
        'driver_total_paid': driver_total_paid,
        'items': items,
        'item_number': item_number
    }
    return render(request, "operationsapp/operations_view_driver_payments.html", context)
    
##############################################    
# Receptionist view driver payments
##########################################
def receptionist_view_driver_payments(request):
    
     # when sending SMS to a driver
    if request.method == 'POST':
        message = request.POST['sms_message']
        driv_name=request.POST['driver_name']
        contact=get_object_or_404(Driver,driver_name=driv_name).driver_contact
        
        # Your Account Sid and Auth Token from twilio.com/console
        custome_message="CANON INNOVATIONS LTD,\n"+"Dear "+driv_name+",\n"+message
        
        message_number=contact.lstrip("0")
        
        
        #SENDING MESSAGES
        
        post_data={'user':'canon','password':'mediat*45TYZ','sender':'CANON','message':custome_message,'reciever':'256'+message_number}
        
        post_response=requests.post(url='http://boxuganda.com/api.php',data=post_data)
        
        sms_balance=requests.get(url='http://boxuganda.com/balance.php?user=canon&password=mediat*45TYZ')
        
        message2="You have successfully sent a message to "+driv_name+","+"  Your SMS balance is:"+sms_balance.text+"SMS's"
        
        all_drivers = Driver.objects.all()
        # loop through all drivers available
        for driver in all_drivers:
    
            driver_name = driver.driver_name
            driver_id = driver.id
            driver_car = driver.attached_car
            driver_balance = driver.driver_monthly_payment
    
            # calculating total paid so far
            total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(
                total_amount_paid=models.Sum("paid_amount"))
            total_paid = total["total_amount_paid"]
            report_item = Driver_Payment_Report()
            report_item.driver_name = driver_name
            report_item.amount_paid = total_paid
            report_item.balance = driver_balance
            report_item.driver_car = driver_car
    
            # first check for availability of an object(filtering)
            if Driver_Payment_Report.objects.filter(driver_name=driver_name):
                Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,
                                                                                     balance=driver_balance)
    
            else:
                report_item.save()
    
        items = Driver_Payment_Report.objects.all()
        item_number = items.count()
    
        # calculating the total balance
        total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]
    
        # calculating the total payments
        total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]
        
        context = {'message':message2,
        'driver_total_balance': driver_total_balance,
        'driver_total_paid': driver_total_paid,
        'items': items,
        'item_number': item_number
        }
        return render(request, "receptionistapp/receptionist_view_driver_payments.html", context)
    
    all_drivers = Driver.objects.all()
    # loop through all drivers available
    for driver in all_drivers:

        driver_name = driver.driver_name
        driver_id = driver.id
        driver_car = driver.attached_car
        driver_balance = driver.driver_monthly_payment

        # calculating total paid so far
        total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(
            total_amount_paid=models.Sum("paid_amount"))
        total_paid = total["total_amount_paid"]
        report_item = Driver_Payment_Report()
        report_item.driver_name = driver_name
        report_item.amount_paid = total_paid
        report_item.balance = driver_balance
        report_item.driver_car = driver_car

        # first check for availability of an object(filtering)
        if Driver_Payment_Report.objects.filter(driver_name=driver_name):
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,
                                                                                 balance=driver_balance)

        else:
            report_item.save()

    items = Driver_Payment_Report.objects.all()
    item_number = items.count()

    # calculating the total balance
    total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
    driver_total_balance = total_bal["total_bal"]

    # calculating the total payments
    total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
    driver_total_paid = total_pai["total_pai"]


    context = {
        'driver_total_balance': driver_total_balance,
        'driver_total_paid': driver_total_paid,
        'items': items,
        'item_number': item_number
    }
    return render(request, "receptionistapp/receptionist_view_driver_payments.html", context)


#########################################################
# operations view driver checklist
#########################################################   
def operations_view_driver_checklist(request):
    items=Driver_checklist.objects.all()
    return render(request,'operationsapp/operations_view_driver_checklist.html',{'items':items})
    
    
###########################################################
# operations add driver checklist
################################################################
def operations_add_driver_checklist(request):
    if request.method=="POST":
        form=DriverCheckListForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            items=Driver_checklist.objects.all()
            info="Successfully added a checklist"
            return render(request,'operationsapp/operations_view_driver_checklist.html',{'info':info,'items': items})
    else:
        form=DriverCheckListForm()
        return render(request, 'operationsapp/operations_add_driver_checklist.html', {'form':form})  
    
    form=DriverCheckListForm()
    return render(request,'operationsapp/operations_add_driver_checklist.html',{'form':form})
    
###################################################################
# operations edit driver checklist
###############################################################
def operations_edit_driver_checklist(request,pk):
    item=get_object_or_404(Driver_checklist,pk=pk)
    
    if request.method=="POST":
        form=DriverCheckListForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('operations_view_driver_checklist')
    
    else:
        form=DriverCheckListForm(instance=item)
    return render(request, 'operationsapp/operations_edit_driver_checklist.html', {'form':form})

##############################################################
# operations delete driver cheklist
#################################################################

def operations_delete_driver_checklist(request,pk):
    Driver_checklist.objects.filter(id=pk).delete()
    items=Driver_checklist.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_driver_checklist.html', context)



    

###################################################
# accountant home
#######################################################

def accountant_home(request):
    return render(request, 'accountantapp/accountant_home.html')


################################################
# accountant view driver payments
######################################################
def accountant_view_driver_payments(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, 'accountantapp/accountant_view_driver_payments.html', context)


###########################################
# accountant make driver payments
#######################################

def accountant_make_driver_payments(request):
    
    if request.method=="POST" and 'receipt_search_form' in request.POST:
        driver_name = request.POST['driver_name']
        driver_id=get_object_or_404(Driver,driver_name=driver_name).id
        
        all_payment_receipts=DriverPayment.objects.filter(driver_name=driver_id)
        
        receipt_number=all_payment_receipts.count()
        
        #the payment form
        form=DriverPaymentForm()
        
        #getting all the drivers
        drivers=Driver.objects.all()
        
        context={'receipt_number':receipt_number,'driver_name':driver_name,'receipt_number':receipt_number,'all_payment_receipts':all_payment_receipts,'form':form,'drivers':drivers}
        return render(request, 'accountantapp/accountant_make_driver_payments.html',context)

    
    if request.method=="POST" and 'payment_form' in request.POST:
        form=DriverPaymentForm(request.POST)
        if form.is_valid():
            #updating the driver balance
            Driver.objects.filter(driver_name=form.cleaned_data['driver_name'].driver_name)\
               .update(driver_monthly_payment=F('driver_monthly_payment')-form.cleaned_data['paid_amount'])

            #saving payment data
            form.save()
            return redirect('accountant_make_driver_payments')
    else:
        #the payment form
        form=DriverPaymentForm()
        
        #getting all the drivers
        drivers=Driver.objects.all()

        # looking for all available payments
        #items = DriverPayment.objects.all()
        
        try:
            items=DriverPayment.objects.latest('id')
        except DriverPayment.DoesNotExist:
            items = None
        context = {'items': items,'form':form,'drivers':drivers}

    return render(request, 'accountantapp/accountant_make_driver_payments.html',context)


##############################################################
# accountant delete driver payment
###################################################################
def accountant_delete_driver_payment(request, pk):
    
    payment_object=get_object_or_404(DriverPayment, pk=pk)
    
    driver_id=payment_object.driver_name.id
    
    amount_paid=payment_object.paid_amount
    
        #updating the driver balance
    Driver.objects.filter(pk=driver_id).update(driver_monthly_payment=F('driver_monthly_payment')+amount_paid)
    
    
    #delete payment object
    DriverPayment.objects.filter(id=pk).delete()
        #the payment form
    form=DriverPaymentForm()
    
    #getting all the drivers
    drivers=Driver.objects.all()
    
    #message
    message="you have delete a payment"

    # looking for all available payments
    #items = DriverPayment.objects.all()
    
    try:
        items=DriverPayment.objects.latest('id')
    except DriverPayment.DoesNotExist:
        items = None
    context = {'items': items,'form':form,'drivers':drivers,'message':message}
    

    return render (request, 'accountantapp/accountant_make_driver_payments.html',context)



############################################
# generate driver payment receipt
################################################
class generate_driver_payment_receipt(View):

    def get(self, request,pk):
        payment_item = get_object_or_404(DriverPayment, pk=pk)
        today = timezone.now()
        params = {
            'payment_item':payment_item,
            'today': today,
            'request': request
        }
        return Render.render('accountantapp/driver_receipt.html', params)


######################################################
# accountant generate driver financial report
##############################################################
class accountant_generate_driver_financial_report(View):
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
        return Render.render('accountantapp/accountant_driver_financial_report.html', params)


            

#########################################
# display_driver_financial statement
##########################################

def accountant_display_driver_financial_statement(request, driver_name):
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
    return render(request,'accountantapp/accountant_display_driver_financial_statement.html', params)


#####################################################
# operations display driver financial statement
#########################################################

def operations_display_driver_financial_statement(request, driver_name):
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
    return render(request,'operationsapp/operations_display_driver_financial_statement.html', params)
    
    
    
#########################################
# receptionist display driver financial statement
##############################################
def receptionist_display_driver_financial_statement(request, driver_name):
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
    return render(request,'receptionistapp/receptionist_display_driver_financial_statement.html', params)




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
    
        return  render(request, "accountantapp/driver_general_financial_report.html",context)
    
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

    return render(request, "accountantapp/driver_general_financial_report.html",context)

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
        return Render.render('accountantapp/print_general_financial_report.html', params)
        
        
        
        
#####################################################
# operations handle complaint
#####################################################
def operations_handle_complaint(request,pk):

    complaint=get_object_or_404(Complaints,pk=pk)
    Complaints.objects.filter(pk=pk).update(forwarded_status='CLEARED')
    Complaints.objects.filter(pk=pk).update(handled_status='HANDLED')

    items = Complaints.objects.filter(forwarded_status='FORWARDED')
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_complaints.html", context)
#########################################################
# operations view car details
##########################################################
def operations_view_car_details(request,pk):
    #driver
    driver=get_object_or_404(Driver,pk=pk)

    #attached car
    specific_car=driver.attached_car

    context={'specific_car':specific_car,}

    return render(request, "operationsapp/operations_view_car_details.html",context)
    
def receptionist_view_car_details(request,pk):
    #driver
    driver=get_object_or_404(Driver,pk=pk)

    #attached car
    specific_car=driver.attached_car

    context={'specific_car':specific_car,}

    return render(request, "receptionistapp/receptionist_view_car_details.html",context)    
    
    
    

######################################################
# operations generate driver financial statement
############################################################
class generate_operations_driver_financial_statement(View):
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
            'today': today,}

        return Render.render('operationsapp/operations_driver_financial_statement.html', params)




##################################
# viewing of monthly archives
#################################

def view_archives(request):


    return render(request, 'operationsapp/view_archives.html')


##############################################
# accountant edit driver receipts
######################################################

def accountant_edit_driver_receipts(request,pk):

    item=get_object_or_404(DriverPayment,pk=pk)
    if request.method=="POST":
        form=DriverPaymentForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('accountant_make_driver_payments')
    else:
        form=DriverPaymentForm(instance=item)
        context={
        'form':form
        }

    return render(request,'accountantapp/accountant_edit_item.html',context)

############################################################
# operations view driver details
##############################################################
def operations_view_driver_details(request,pk):
    
    specific_driver=get_object_or_404(Driver,pk=pk)
    
    context={
        'specific_driver':specific_driver
    }
    
    
    return render(request,'operationsapp/operations_view_driver_details.html',context)

###########################################################
# receptionist view driver details
###########################################################
def receptionist_view_driver_details(request,pk):
    
    specific_driver=get_object_or_404(Driver,pk=pk)
    
    context={
        'specific_driver':specific_driver
    }
    
    
    return render(request,'receptionistapp/receptionist_view_driver_details.html',context)
  
    
######################################
# Searching for archived report
#############################################
    
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
        return render(request,"accountantapp/accountant_driver_payment_archive.html",context)
        

    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accountantapp/accountant_driver_payment_archive.html",context)





########################################################
# printing archived monthly reports
########################################################
    
class accountant_driver_payment_archive_print(View): 
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

        return Render.render('accountantapp/accountant_driver_payment_archive_print.html', context) 
    
    

##########################################
# Searching for the payment receipts
####################################################

def accountant_driver_payment_archived_receipt(request):
           # when we search for monthly archived receipts for customers
    if request.method == 'POST':
        receipt_year = request.POST['receipt_year'] 
        receipt_month=request.POST['receipt_month']
        receipt_driver=request.POST['receipt_driver']
        
        driver_id=get_object_or_404(Driver, driver_name=receipt_driver).id
    
        archived_receipts=DriverPayments_Archive.objects.filter(month=receipt_month, year=receipt_year,driver_name=driver_id)
        
        # calculating the total payments
        total_pai = archived_receipts.aggregate(total_pai=models.Sum("paid_amount"))
        driver_total_paid = total_pai["total_pai"]
        
        #getting number of payments
        payments=archived_receipts.count()
        
        #getting the cycle balance
        payment_ref=get_object_or_404(Driver, driver_name=receipt_driver).driver_monthly_payment_ref
        
       # cycle_balance=payment_ref-driver_total_paid
        if driver_total_paid==None:
            cycle_balance=payment_ref
        
        else:
            cycle_balance=payment_ref-driver_total_paid
        
        
        
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        drivers=Driver.objects.all()
        context={'payment_ref':payment_ref,'cycle_balance':cycle_balance,'payments':payments,'archived_receipts':archived_receipts,'months':months,'years':years,'drivers':drivers,'driver_total_paid':driver_total_paid,'receipt_year':receipt_year,'receipt_month':receipt_month,'receipt_driver':receipt_driver}
        return render(request,"accountantapp/accountant_driver_payment_archived_receipt.html",context)
            
    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November', 'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accountantapp/accountant_driver_payment_archived_receipt.html",context)


##################################################################
# printing driver archived monthly statements
#######################################################################
class print_archived_driver_statement(View):
    def get(self,request,receipt_month,receipt_year,receipt_driver):
        #getting the driver id
        driver_id=get_object_or_404(Driver, driver_name=receipt_driver).id
        
        #getting all the archived receipts
        archived_receipts=DriverPayments_Archive.objects.filter(month=receipt_month, year=receipt_year,driver_name=driver_id)

        # calculating the total payments
        total_pai = archived_receipts.aggregate(total_pai=models.Sum("paid_amount"))
        driver_total_paid = total_pai["total_pai"]
        
        #getting number of payments
        payments=archived_receipts.count()
        
        #getting the current time zone
        today = timezone.now()
        
        #getting the cycle balance
        payment_ref=get_object_or_404(Driver, driver_name=receipt_driver).driver_monthly_payment_ref
        
        cycle_balance=payment_ref-driver_total_paid
        
        context={
            'payment_ref':payment_ref,
            'cycle_balance':cycle_balance,
            'today':today,
            'payments':payments,
            'archived_receipts':archived_receipts,
            'driver_total_paid':driver_total_paid,
            'receipt_month':receipt_month,
            'receipt_year':receipt_year,
            'receipt_driver':receipt_driver
        }
        
        
        return Render.render('accountantapp/print_archived_driver_statement.html',context)

    

################################

 #   ACCOUNTANT DEFS  #
#############################

def accountantindex(request):
    return render(request,'accountantapp/Accprofile.html')

def accountant_profile(request):
    return render(request, 'accountantapp/Accprofile.html')

    ####################################################
    #        ENTERING RECORDS INTO THE DATABASE        #
    ####################################################
    

def add_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_viewstaff')
    else:
        form = StaffForm()
        return render(request, 'accountantapp/add_staff.html', {'form': form})

def display_viewstaff(request):
    all_staff =Staff.objects.all()
    return render(request,'accountantapp/display_staff.html',{'all_staff': all_staff})            

 # payment of salaries
def pay_salary(request):
    if request.method=="POST":
        form=SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salaryreport')
    else:
        form=SalaryForm()
        return render(request, 'accountantapp/add_new.html',{'form':form})

# recording the major expenditures
def enter_expenditure(request):
    if request.method=="POST":
        form=SpendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('expenditurereport')
    else:
        form=SpendForm()
        items = Spend.objects.all()
        context = {'items': items, 'form': form }
        return render(request, 'accountantapp/pay_expenditure.html',context)



  #recording small expenses
def enter_sundryexpense(request):
    if request.method=="POST":
        form=SundryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('sundryreport')
    else:
        form=SundryForm()
        return render(request, 'accountantapp/add_new.html',{'form':form})

#############################################################        
# EDITTING THE FIELDS THE ENTRIES THAT HAVE BEEN RECORDED   #
#############################################################
def edit_payment(request, pk):
    item = get_object_or_404(Spend, pk=pk)
    if request.method == "POST":
        form = SpendForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expenditurereport')
    else:
        form = SpendForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })

def edit_salary(request, pk):
    item = get_object_or_404(Salary, pk=pk)
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('salaryreport')
    else:
        form = SalaryForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })

def edit_sundry(request, pk):
    item = get_object_or_404(Sundry, pk=pk)
    if request.method == "POST":
        form = SundryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sundryreport')
    else:
        form = SundryForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })
    
def delete_sundry(request, pk):
    Sundry.objects.filter(id-pk).delete()
    items.Sundry.objects.all()
    context = {'items': items}
    return render (request, 'sundryindex.html', context)
    
    
def delete_salary(request,pk):
    items= Spend.objects.filter(id=pk).delete()
    items.Salary.objects.all()
    context = { 'items':items}
    return render(request, 'accountantapp/salaryindex.html', context)
    
def delete_payment(request,pk):
    Spend.objects.filter(id=pk).delete()
    items=Spend.objects.all()
    
    context = { 'items':items}
    return render(request, 'accountantapp/expenditureindex.html', context)
    
        ####################################################
        #                VIEWING  THE REPORTS              #
        ####################################################

''''def display_viewstaff(request):
    all_staff = Staff.objects.all()
    return render(request,'accountantapp/accountantindex.html',{'Staffs': all_staff})'''

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
  return render(request, 'accountantapp/salaryindex.html', context)

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
  return render(request, 'accountantapp/expenditureindex.html', context)

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
  return render(request, 'accountantapp/sundryindex.html', context)


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
      return Render.render('accountantapp/expenditurepdf.html', expensecontext)

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
        return Render.render('accountantapp/pdf.html', salarycontext)

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
          'month': month,
          'today': today,
          'sundry': sundry,
          'request': request,
          'totalsundry': totalsundry,
        }
        return Render.render('accountantapp/sundrypdf.html', sundrycontext)
#printing staff details        
class accountant_print_staff(View):     
    def get(self, request):
        print_staff=Staff.objects.all() 
        today = timezone.now()
        context={
          'print_staff':print_staff,'today':today
        }
        return Render.render('accountantapp/accountant_print_staff.html',context )




      ####################################################
      #       PRINTING THE RECEIPTS                      #
      ####################################################

class expensereceipt(View):
    def get(self, request, pk):
        expense = get_object_or_404(Spend,pk=pk)
        today = timezone.now()
        expensecontext = {
          'today': today,
          'expense': expense,
          'request': request,
        }
        return Render.render('accountantapp/expensereceipt.html', expensecontext)

class salaryreceipt(View):
    def get(self, request, pk):
        salary = get_object_or_404(Salary,pk=pk)
        today = timezone.now()
        salarycontext = {
          'today': today,
          'salary': salary,
          'request': request,
        }
        return Render.render('accountantapp/salaryreceipt.html', salarycontext)

class sundryreceipt(View):
    def get(self, request,pk):
        sundry = get_object_or_404(Sundry, pk=pk)
        today = timezone.now()
        sundrycontext = {
          'today': today,
          'sundry': sundry,
          'request': request,
        }
        return Render.render('accountantapp/sundryreceipt.html', sundrycontext)

  ####################################################
  #        ARCHIVING OF THE MONTHLY REPORTS          #
  ####################################################

def salaryarchive(request):
    salaryarchived = SalaryReportArchive.objects.all().order_by('-Date')
    total = SalaryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'salaryarchived': salaryarchived
               }
    return render(request, 'accountantapp/salaryarchive.html', context)

def expenditurearchive(request):
    expensesarchived = ExpensesReportArchive.objects.all().order_by('-Date')
    total = SalaryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'expensesarchived':expensesarchived
    }
    return render(request, 'accountantapp/expenditurearchive.html', context)

# calculating totals in sundryexpense report
def sundryarchive(request):
    sundryarchived = SundryReportArchive.objects.all().order_by('-Date')
    total = SundryReportArchive.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
        'total_amount':total_amount,
        'sundryarchived': sundryarchived
               }
    return render(request, 'accountantapp/sundryarchive.html', context)



 

  ############################################################
   # SUBMISSION OF MONTHLY REPORTS TO BE ARCHIVED              #
    ############################################################

#####################
# EXPENSES ARCHIVING#
#####################
def expenditurereport (request):
    if request.method=='POST':
        archived_year=request.POST['archived_year']
        archived_month = request.POST['archived_month']

        #all the available expense in the expenses table
        all_expenses = Spend.objects.all()

        for expense in all_expenses:
            date=expense.Date
            amount=expense.Amount
            reason=expense.ReasonForPayment
            name=expense.PaymentMadeTo

            # the expense archive object
            expense_archiveobj=ExpensesReportArchive()

            #attached values to expense_archiveobj
            expense_archiveobj.Name=name
            expense_archiveobj.Date=date
            expense_archiveobj.Amount=amount
            expense_archiveobj.Reason=reason
            expense_archiveobj.year=archived_year
            expense_archiveobj.month=archived_month

            expense_archiveobj.save()

        #deleting all the expense from reports table


        #paid = Spend.objects.all().aggregate(Sum('Amount'))
        all_expenses.delete()

        message="The expenses report has been made"
        context={
                 'message':message,
                 }

        return render(request, 'accountantapp/expenditureindex.html', context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'August', 'September',
              'October', 'November',
              'December']
    years = [2019, 2020]
    items =Spend.objects.all()
    total = Spend.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    context = {
         'total_amount':total_amount,
        'items': items,
        'months':months,
        'years':years,


    }
    return render(request, 'accountantapp/expenditureindex.html', context)

def salaryreport (request):
    if request.method=='POST':
        archived_year=request.POST['archived_year']
        archived_month = request.POST['archived_month']

        #all the available expense in the expenses table
        all_expenses = Salary.objects.all()
        for expense in all_expenses:
            date=expense.Date
            Manth = expense.Month
            amount=expense.Amount
            salary_type=expense.Salary_Type
            name = expense.Staff

            # the expense archive object
            expense_archiveobj=SalaryReportArchive()

            #attached values to expense_archiveobj
            expense_archiveobj.Staff = name
            expense_archiveobj.Date=date
            expense_archiveobj.Month=Manth
            expense_archiveobj.Amount=amount
            expense_archiveobj.Salary_Type=salary_type
            expense_archiveobj.archivedyear= archived_year
            expense_archiveobj.archivedmonth =archived_month

            expense_archiveobj.save()

        #deleting all the expense from reports table
        all_expenses.delete()

        message="The expenses report has been made"
        context={'message':message}

        return render(request, 'accountantapp/salaryindex.html', context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'August', 'September',
              'October', 'November',
              'December']
    years = [2019, 2020]
    total = Salary.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    items =Salary.objects.all()
    context = {
        'total_amount':total_amount,
        'items': items,
        'months':months,
        'years':years,
    }
    return render(request, 'accountantapp/salaryindex.html', context)

def sundryreport (request):
    if request.method=='POST':
        archived_year=request.POST['archived_year']
        archived_month = request.POST['archived_month']
        #all the available expense in the expenses table
        all_expenses = Sundry.objects.all()
        for expense in all_expenses:
            date=expense.Date
            amount=expense.Amount
            reason=expense.ReasonForPayment
            name=expense.PaymentMadeTo

            # the expense archive object
            expense_archiveobj=SundryReportArchive()

            #attached values to expense_archiveobj
            expense_archiveobj.Name=name
            expense_archiveobj.Date=date
            expense_archiveobj.Amount=amount
            expense_archiveobj.Reason=reason
            expense_archiveobj.year=archived_year
            expense_archiveobj.month=archived_month

            expense_archiveobj.save()

        #deleting all the expense from reports table
        all_expenses.delete()

        message="The expenses report has been made"
        context={'message':message}

        return render(request, 'accountantapp/sundryindex.html', context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'August', 'September',
              'October', 'November',
              'December']
    years = [2019, 2020]

    total = Sundry.objects.aggregate(totals=models.Sum("Amount"))
    total_amount = total["totals"]
    items =Sundry.objects.all()
    context = {
        'total_amount':total_amount,
        'items': items,
        'months':months,
        'years':years,
    }
    return render(request, 'accountantapp/sundryindex.html', context)

# searching for the archives
def expensesarchivessearch(request):
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
        return render(request, "accountantapp/expenditurearchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October', 'November', 'November', 'December']
    years = [2019, 2020]
    expenses=ExpensesReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'expenses': expenses}
    return render(request, "accountantapp/expenditurearchive.html", context)


def salaryarchivessearch(request):
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
        return render(request, "accountantapp/salaryarchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October',  'November', 'December']
    years = [2019, 2020]

    salary=SalaryReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'salary': salary}
    return render(request, "accountantapp/salaryarchive.html", context)

def sundryarchivessearch(request):
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
        return render(request, "accountantapp/sundryarchive.html", context)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'August', 'September','October', 'November', 'November', 'December']
    years = [2019, 2020]

    sundry=SundryReportArchive.objects.all()

    context = {'months': months,
               'years': years,
               'sundry': sundry}
    return render(request, "accountantapp/sundryarchive.html", context)
    

   ####################################################
    #        GENERATING REPORTS IN FORM OF ANNUAL PDFS #
    ####################################################

# Printing Expenditure archived Report
class expenditurearchivepdf(View):
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
        return Render.render('accountantapp/expenditurearchivepdf.html', expensecontext)


# Printing Salaries archived Report
class salaryarchivepdf(View):
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
        return Render.render('accountantapp/salaryarchivepdf.html', salarycontext)


# Printing Sundry Expenses archived Report
class sundryarchivepdf(View):
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
        return Render.render('accountantapp/sundryarchivepdf.html', sundrycontext)






































