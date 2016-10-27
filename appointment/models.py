from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

# Create your models here.
class Appointment(models.Model):
    appointment_datetime=models.DateTimeField('appointment time and date',default=timezone.now())
    fresh_or_review=models.BooleanField(default=False)
    appointment_problem=models.TextField(max_length=100,default='no appointment remove this')
    #should use charfiled instead? come back and change if problem
    def __unicode__(self):
        return self.appointment_problem

class Patient(models.Model):
    appointment=models.ForeignKey(Appointment,unique=True,blank=True,null=True)
    patient_name=models.CharField(max_length=30)
    patient_age=IntegerRangeField(min_value=1,max_value=120)
    MALE='Male'
    FEMALE='Female'
    SEX_CHOICES=((MALE,'Male'),(FEMALE,'Female')) 
    #you gave human readable form same trouble?? remove or keep? check later
    patient_sex=models.CharField(max_length=6,choices=SEX_CHOICES)
    patient_email=models.EmailField(max_length=75)
 #   phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
  #  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    patient_phone=PhoneNumberField()
    #models.CharField(max_length=16,validators=[phone_regex], blank=True) # validators should be a list
    #temporary check your email and confirm with the link other optns
    def __unicode__(self):
        return self.patient_name


    
    