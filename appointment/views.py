from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from appointment.models import Patient,Appointment
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime,timedelta
import phonenumbers
from django.core.mail import EmailMessage
from django.views.generic import View
# Create your views here.
class Index(View):

    def get(self,request):
        dt=[]
        now=timezone.now()
        one_day=timedelta(days=1)
        two_day=timedelta(days=2)
        h=timedelta(hours=1)
        while now.hour!=int(9): #start time
            now=now-h
        s=timedelta(seconds=1)
        while now.second != int(0):
            now=now-s
        m=timedelta(minutes=1)
        while now.minute!=int(0):
            now=now-m
        m=timedelta(minutes=10)
        dt.append(now)
        won=now
        while won.hour!=int(13): #check 1 loop logic
            won=won+m
            dt.append(won)
        dt.pop()    
        for x in xrange(len(dt)):
            won=dt[x]+one_day
            dt.append(won)
            won=dt[x]+two_day
            dt.append(won)  #now dt filled with all possible appointments remove
            #one's already booked i.e in database
        a=Appointment.objects.all()
        a=[x.appointment_datetime for x in a]
        display_list=[str(x) for x in list(set(dt)-set(a))] #remove already booked appointments
        display_list.sort()
        for x in xrange(len(display_list)):
            bugfix=list(display_list[x])
            bugfix=bugfix[:19]
            display_list[x]="".join([y for y in bugfix])
        context={'display_list': display_list}
        return render(request,'appointment/index.html',context)
    
    
class Form_handle(View):
    
    def post(self,request):
        """create patient object check wether it is already in db
        if it is don't store check wether the appointment is 
        within 15 days of the previous one if it is 'review' 
        else it is 'fresh'.Retrieve the particular patient 
        object from db create the appointment object and 
        point it to the patient
        if patient ain't in db store patient and create
        appointment pointing to that patient and store it"""
        F=request.POST
        try:
            pp=Patient.objects.get(patient_name=F['name'],
                                    patient_email=F['email']
                    )
            try:
                app=pp.appointment
            except Appointment.DoesNotExist:
                pass
            comp=datetime.strptime(F['datetime'],'%Y-%m-%d %H:%M:%S')
            if comp.day-app.appointment_datetime.day <= 15: #review
                store_app=Appointment(
                    appointment_datetime=comp,
                    fresh_or_review=True,
                    appointment_problem=F['problem'])
                store_app.save()
                pp.appointment=store_app
                pp.save()
                mail_to_doctor=EmailMessage('appointment for %s'%pp.patient_name,
                    store_app.appointment_problem,
                    to=['spvijayal@gmail.com'] 
                )
                mail_to_doctor.send() #returns 1 on success or SMTP standard errors
                mess='''Respected Sir/Madam,
                                           Your review appointment is scheduled on %s'''%F['datetime']
                mail_to_patient=EmailMessage('clinic\'s name',
                    mess,
                to=['%s'%pp.patient_email]
                
                )
                mail_to_patient.send()

            else:
                store_app=Appointment(
                appointment_datetime=comp,
                appointment_problem=F['problem'])
                store_app.save()
                pp.appointment=store_app
                pp.save()
                mail_to_doctor=EmailMessage('appointment for %s'%pp.patient_name,
                    store_app.appointment_problem,
                    to=['spvijayal@gmail.com'] 
                )
                mail_to_doctor.send()
                mess='''Respected Sir/Madam,
                                           Your fresh appointment is scheduled on %s'''%F['datetime']
                mail_to_patient=EmailMessage('clinic\'s name',
                    mess,
                to=['%s'%pp.patient_email]
                
                )
                mail_to_patient.send()
                
            return HttpResponseRedirect('results/')
            
        except Patient.DoesNotExist:
            try:
                z=phonenumbers.parse(F['phonenum'],"IN")
            except phonenumbers.NumberParseException:
                cont={'error_message': '    Invalid Phone Number  '}
                return render(request,'appointment/index_l.html',cont)
            if int(F['age']) >= 120 or int(F['age']) < 1:
                con={'error_message': '%s is your age eh !! Nice try'%F['age']}
                return render(request,'appointment/index_l.html',con)
            if len(F['phonenum'][3:])!=10:
                cont={'error_message': '    Invalid Phone Number  '}
                return render(request,'appointment/index_l.html',cont)
            try:
                u=(int(x) for x in F['phonenum'][1:])
                for uu in u:
                    uu=type(uu)
            except ValueError:
                cont={'error_message': '    Invalid Phone Number  '}
                return render(request,'appointment/index_l.html',cont)
            
            if not phonenumbers.is_possible_number(z):
                cont={'error_message': '    Invalid Phone Number  '}
                return render(request,'appointment/index_l.html',cont)
            
            if not phonenumbers.is_valid_number:
                cont={'error_message': '    Invalid Phone Number  '}
                return render(request,'appointment/index_l.html',cont)    
            email_doms=['aol.com','comcast.net','facebook.com',
                        'gmail.com', 'hotmail.com','msn.com'
                        'outlook.com','yahoo.com','yahoo.co.in'
            ]
            if str(F['email']).split('@')[0] == '':
                err_mail={'error_message':'     Invalid email address  '}
                return render(request,'appointment/index_l.html',err_mail)

            if  F['email'].split('@')[1] not in email_doms :
                err_mail={'error_message':'   No support for email by %s'%F['email'].split('@')[1]}
                return render(request,'appointment/index_l.html',err_mail)
            comp=datetime.strptime(F['datetime'],'%Y-%m-%d %H:%M:%S')
            store_app=Appointment(
                        appointment_datetime=comp,
                        appointment_problem=F['problem'])
            store_app.save()
            p=Patient(appointment=store_app,
                       patient_name=F['name'],
                       patient_age=int(F['age']),
                       patient_sex=F['sex'],
                       patient_email=F['email'],
                       patient_phone=F['phonenum'])
            p.save()
            mail_to_doctor=EmailMessage('appointment for %s'%p.patient_name,
                    store_app.appointment_problem,
                    to=['spvijayal@gmail.com'] 
                )
            mail_to_doctor.send()
            
            mess='''Respected Sir/Madam,
                                        We are glad to offer our services,Kindly visit the clinic on %s'''%F['datetime']
            mail_to_patient=EmailMessage('clinic\'s name',
                    mess,
                to=['%s'%p.patient_email]
                
            )
            mail_to_patient.send()

            return HttpResponseRedirect('results/')   

class Results(View):
    def get(self,request):
            return render(request,'appointment/index_l.html')
    
    
     
    