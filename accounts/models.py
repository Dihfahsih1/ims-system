from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

# Create your models here.

class UserProfileManager(models.Manager):
    pass

class UserProfile(models.Model):
    ROLES = (
        ('', ''),
        ('Executive', 'Executive'),
        ('Manager', 'Manager'),
        ('Receptionist', 'Receptionist'),
        ('Accountant', 'Accountant'),
        ('Operations', 'Operations'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLES, default='', max_length=20)
    phone = models.IntegerField(default='+256701345376')
    hired_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)



    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs ['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Staff(models.Model):
    Duties = (
        ('Others', 'Others'),
        ('Executive', 'Executive'),
        ('Manager', 'Manager'),
        ('Receptionist', 'Receptionist'),
        ('Accountant', 'Accountant'),
        ('Operations', 'Operations'),
    )
    
    GENDER_CHOICES = (
       ('M', 'Male'),
       ('F', 'Female'),
    )

    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateField(default='2019-03-12')
    gender = models.CharField(choices=GENDER_CHOICES, default='Male', max_length=10)
    address = models.CharField(max_length=200)
    phone = models.IntegerField(default='+256701345376')
    role = models.CharField(choices=Duties, default='', max_length=20)
    duties = models.TextField(max_length=200)
    salary = models.IntegerField(default='300000')
    
    def __str__(self):
        return self.first_name+" "+self.last_name