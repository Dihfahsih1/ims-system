from django.db import models
from django.utils.timezone import now
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import  User
from django.db.models import Sum

# Create your models here.

class Car(models.Model):
    car_name=models.CharField(max_length=100)
    car_model=models.CharField(max_length=100)
    car_engine_no=models.CharField(max_length=100)
    car_registration_no=models.CharField(max_length=100)
    car_consumption_rate=models.CharField(max_length=100)
    car_image=models.ImageField(max_length=100)
    availability=models.CharField(max_length=100,default='AVAILABLE')


    def __str__(self):
        return self.car_registration_no


class Driver(models.Model):
    driver_name=models.CharField(max_length=100)
    driver_next_of_kin=models.CharField(max_length=100)
    driver_next_of_kin_contact=models.CharField(max_length=100)
    next_of_kin_national_id_image=models.ImageField(max_length=100)
    driver_licence_no=models.CharField(max_length=100)
    driver_contact=models.CharField(max_length=100)
    driver_email=models.EmailField(max_length=100,blank=True)
    driver_image=models.ImageField(max_length=100)
    driver_monthly_payment=models.FloatField(default=1132000.0)
    driver_permit_or_nationalID_image=models.ImageField(max_length=100)
    attached_car=models.ForeignKey(Car,on_delete=models.PROTECT)
    driver_monthly_payment_ref=models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.driver_monthly_payment_ref=self.driver_monthly_payment
        super(Driver, self).save(*args, **kwargs)


    def __str__(self):
        return  'Driver Name:{0}   Assigned Vehicle:{1}'.format(self.driver_name,self.attached_car)


class Complaints(models.Model):
    date=models.DateField(default=now())
    complaint=models.TextField(max_length=500)
    complainant=models.ForeignKey(Driver,on_delete=models.PROTECT,blank=True,null=True)
    other_complainant=models.CharField(max_length=100,blank=True,null=True)
    forwarded_status=models.CharField(max_length=100,default="NOT FORWARDED")
    handled_status=models.CharField(max_length=100,default="NOT HANDLED")

    def __str__(self):
        return self.complaint

class DriverPayment(models.Model):
    date=models.DateField(default=now())
    driver_name=models.ForeignKey(Driver,on_delete=models.PROTECT)
    paid_amount=models.FloatField(default=0.0)
    paid_by=models.CharField(max_length=100)
    received_by=models.CharField(max_length=100)


    def __str__(self):
        return 'Driver:{0} Amount:{1}'.format(self.driver_name,self.paid_amount)


class Driver_Payment_Report(models.Model):
    date=models.DateField(default=now())
    driver_name=models.CharField(max_length=100, default='name',null=True)
    driver_car=models.CharField(max_length=100,default='car',null=True)
    amount_paid=models.FloatField(default=0.0,null=True)
    balance=models.FloatField(default=0.0,null=True)

    def __str__(self):
        return ' Driver_Name:{1} Amount_paid:{2} Balance: {3}'.format(self.driver_name,self.amount_paid,self.balance)


class DriverPayments_Archive(models.Model):
    date=models.DateField(default=now())
    month=models.CharField(max_length=100,null=True)
    year=models.CharField(max_length=100,null=True)
    driver_name = models.ForeignKey(Driver, on_delete=models.PROTECT)
    paid_amount = models.FloatField(default=0.0)
    paid_by = models.CharField(max_length=100)
    received_by = models.CharField(max_length=100)

    def __str__(self):
        return 'Driver:{0} Amount:{1}'.format(self.driver_name, self.paid_amount)


class Driver_payment_Reports_Archive(models.Model):
    date=models.DateField(default=now())
    month=models.CharField(max_length=100,null=True)
    year=models.CharField(max_length=100,null=True)
    driver_name=models.CharField(max_length=100, default='name',null=True)
    driver_car=models.CharField(max_length=100,default='car',null=True)
    amount_paid=models.FloatField(default=0.0,null=True)
    balance=models.FloatField(default=0.0,null=True)

    def __str__(self):
        return ' Driver_Name:{1} Amount_paid:{2} Balance: {3}'.format(self.driver_name,self.amount_paid,self.balance)


class Driver_checklist(models.Model):
    date=models.DateField(default=now())
    driver_name=models.ForeignKey(Driver,on_delete=models.PROTECT)
    checklist_file=models.FileField(upload_to = 'checklists', default = True)
    
    def __str__(self):
        return self.checklist_file 

    



#################################
#rest of the models for the accounts section
#####################################



class Salary(models.Model):
    choices = (
        ('ALLOWANCE','Pay Allowances'),
        ('Salary','Monthly Salary'),
        ('Advance', 'Pay Advances'),
        ('Commission', 'Pay Commission')
    )
    months = (
        ('January','January'),('February','February'),('March', 'March'),('April', 'April')
        ,('May','May'),('June', 'June'),('July', 'July'),('August','August'),
        ('September', 'September'),('October', 'October'),('November','November'),('December', 'December')
    )
    Date = models.DateField(default=now())
    Salary_Type = models.CharField( max_length=12,choices=choices,default="Choose Salary Type")
    Staff = models.ForeignKey('accounts.Staff',related_name='+',on_delete=models.PROTECT, blank=False)
    Month = models.CharField(max_length=12,choices=months, default="Month of Pay")
    Amount = models.IntegerField(default=0)
    AmountInWords = models.CharField(max_length=1000, blank=False, default='amount in words')
    def __str__(self):
        return self.Staff

class Sundry(models.Model):
    Date = models.DateField(default=now())
    PaymentMadeTo = models.CharField(max_length=100, default="Type Name", blank=False)
    ReasonForPayment = models.CharField(max_length=500, default="Only relatively small expense")
    Amount = models.IntegerField(default=0)
    AmountInWords = models.CharField(max_length=1000, blank=False, default='amount in words')
    def __str__(self):
        return self.PaymentMadeTo

class Spend(models.Model):
    Date = models.DateField(default=now())
    PaymentMadeTo = models.CharField(max_length=100, default="Type Name", blank=False)
    ReasonForPayment = models.CharField(max_length=1000, default="Type Main Expense" )
    Amount = models.IntegerField(default=0)
    AmountInWords = models.TextField(max_length=500, blank=False,default='amount in words')
    ReceivedBy = models.CharField(max_length=100, blank=False,default='Person Receiving Money')
    ApprovedBy = models.CharField(max_length=100, blank=False,default='Manager-Patrick')

    def __str__(self):
        return self.PaymentMadeTo


##########################################
#REPORT ARCHIVING MODELS AFTER SUBMISSION #
##########################################
class ExpensesReportArchive(models.Model):
    Date = models.DateField(default=now())
    Name = models.CharField(max_length=100, default='Name', null=True)
    Amount = models.FloatField(default=0.0, null=True)
    Reason = models.CharField(max_length=100,null=True)
    ReceivedBy = models.CharField(max_length=100, blank=False, default="Name")
    ApprovedBy = models.CharField(max_length=100, blank=False,default="Name")
    month = models.CharField(max_length=100,null=True)
    year = models.CharField(max_length=100,null=True)

    def __str__(self):
        return 'Name: {1} Reason:{2} Amount:{0}'.format(self.Name,self.Reason, self.Amount)
class SundryReportArchive(models.Model):
    Date = models.DateField(default=now())
    Name = models.CharField(max_length=100, default='Name', null=True)
    Amount = models.FloatField(default=0.0, null=True)
    Reason = models.CharField(max_length=100,null=True)
    ReceivedBy = models.CharField(max_length=100, blank=False, default="Name")
    ApprovedBy = models.CharField(max_length=100, blank=False, default="Name")
    month = models.CharField(max_length=100,null=True)
    year = models.CharField(max_length=100,null=True)

    def __str__(self):
        return 'Name: {1} Reason:{2} Amount:{0}'.format(self.Name,self.Reason, self.Amount)

class SalaryReportArchive(models.Model):
    Date = models.DateField(default=now())
    Salary_Type = models.CharField(max_length=100,null=True)
    Staff = models.CharField( max_length=100,null=True)
    Month = models.CharField(max_length=100,null=True)
    Amount = models.IntegerField(default=0)
    archivedmonth = models.CharField(max_length=100,null=True)
    archivedyear = models.CharField(max_length=100,null=True)

    def __str__(self):
        return 'Name: {1}  Amount:{0}'.format(self.Staff, self.Amount)







