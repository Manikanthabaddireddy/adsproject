#importing  modules  

from django.shortcuts import redirect, render
from django.contrib import messages
from WebApp.forms import Remainder_Modelform, Web_Modelform
from WebApp.forms import Fin_Modelform
from WebApp.models import Finance_Model, Web_Model,Remainder_Model
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

from templates.serializers import Ser
# Create your views here.

# HomePage 
def HomePage(request):
    form = Web_Modelform
    data = {'form':form}
    if request.method=='POST': #if method is POST then execute following statements
        form=Web_Modelform(request.POST)  
        if form.is_valid():
            form.save()
            messages.success(request,('Hey! You have successfully Done'))
        else:
            messages.success(request,('Hey! Form is invalid please check number'))
    return render(request,'index.html',data)


# Finance Screen 
def Fin(request,id):
    s=Web_Model.objects.get(id=id)
    form=Fin_Modelform(instance=s)
    k=Finance_Model.objects.all().order_by('Name')
    if request.method=='POST':
        Fin_form=Fin_Modelform(request.POST)
        if Fin_form.is_valid():
           Fin_form.save()
           messages.success(request,('Hey! You have successfully Done'))
        else:
             messages.success(request,('Hey! Form is existed with this number')) 
    return render(request,'Fin.html',{'form':form,'k':k})

#Finance Data
def Fin_data(request):
    m=Finance_Model.objects.all()
    if request.method=='get':
        n=request.get['Add_Money']
        m=request.get['Total_amount_Received_So_Far']
        if m is None:
           m=n+m
           m.save()
    return render(request,'fin_reports.html',{'m':m})
#Update Finance Data
def Fin_update(request,id):
    s=Finance_Model.objects.get(id=id)
    b=int(s.Add_Money) + int(s.Total_amount_Received_So_Far)
    (s.Total_amount_Received_So_Far)=b
    (s.Add_Money)=0
    form=Fin_Modelform(instance=s) 
    if request.method=="POST":
        form=Fin_Modelform(request.POST,instance=s)
        if form.is_valid():
            form.save()
            messages.success(request,('Hey! You have successfully Updated'))
        else:
             messages.success(request,('Hey! Form is invalid please check number'))

    return render(request,'fin_update.html',{'form':form,'money':b})

# Customer report
def Form_Report(request):
    Form_data=Web_Model.objects.all() #Retreiving All Data From Web_Model(Database)
    data_Form={'Form_data':Form_data}
    return render(request,'report.html',data_Form)

#Existing Form Update
def Update(request,id):
    Form_data=Web_Model.objects.get(id=id)
    update_form=Web_Modelform(instance=Form_data)
    update_data={'update_form':update_form}
    if request.method=='POST':
        update_form=Web_Modelform(request.POST,instance=Form_data)
        if update_form.is_valid: 
           update_form.save()
           messages.success(request,('Hey! You have successfully Updated'))
        else:
             messages.success(request,('Hey! Form is invalid please check number'))
    return render(request,'update.html',update_data)

#Search Bar
def Search(request):
    if request.method=="POST":
        searched=request.POST['searched']
        res=Web_Model.objects.filter(Name=searched) | Web_Model.objects.filter(Calling_status__contains=searched) | Web_Model.objects.filter(Current_status__contains=searched) |  Web_Model.objects.filter(Phone_Number__startswith=searched) | Web_Model.objects.filter(Current_status__contains=searched) |  Web_Model.objects.filter(Comments=searched)
        return render(request,'search.html',{'searched':searched,'result':res})

#Remainder 
def Remainder(request,id):
    m=Web_Model.objects.get(id=id)
    form=Remainder_Modelform(instance=m)
    Remainder_data=Remainder_Model.objects.all().order_by('Name') #Retreiving All Data From Web_Model(Database)
    if request.method=='POST':
        remainder_form=Remainder_Modelform(request.POST)
        if remainder_form.is_valid():
            remainder_form.save()
            messages.success(request,('Hey! You have successfully Done'))
        else:
            messages.success(request,('Hey! Form is invalid please check'))
    return render(request,'remainder.html',{'form':form,'Remainder_data':Remainder_data})

#Remainder Data
def Remainder_Report(request):
    Remainder_data=Remainder_Model.objects.all().order_by('Name') #Retreiving All Data From Web_Model(Database)
    data_Form={'Remainder_data':Remainder_data}
    return render(request,'remainder_report.html',data_Form)

#Remainder Update
def Remainder_Update(request,id):
    form_remainder=Remainder_Model.objects.get(id=id)
    update_form=Remainder_Modelform(instance=form_remainder)
    update_data={'update_form':update_form}
    if request.method=='POST':
        remainder_form=Remainder_Modelform(request.POST,instance=form_remainder)
        if remainder_form.is_valid: 
           remainder_form.save()
           messages.success(request,('Hey! You have successfully Updated'))  
        else:
            messages.success(request,('Hey! Form is already existed!'))
    return render(request,'remainder_update.html',update_data)

#User Login
def login_user(request):
    if request.method=='POST':
        Name = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=Name, password=password)
        if user is not None:
            login(request, user)
            return redirect(HomePage)
        else:
            messages.success(request,('Hey! You entered invalid Name or Password'))
            return render(request,'login.html')
           
    else:
        return render(request,'login.html')

#New User Account
def Sign_up(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        password_2=request.POST['Re_password']
        email=request.POST['email']
        if password==password_2:
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            messages.success(request,('Hey! You have sign-up successfully'))
            return redirect('/')
        else:
            messages.success(request,('Hey! you entered wrong credentials or password miss match'))
            return render(request,'sign_up.html',)
        

    else:
        return render(request,'sign_up.html',)

#installing modules for restapi
from rest_framework.views import APIView
from rest_framework.response import Response
#creating class Based view for RestApi
class Rest(APIView):
    def get(request,self):
        deta=Finance_Model.objects.all()
        s=Ser(deta,many=True)
        return Response(s.data)
        
    
