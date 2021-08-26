from __future__ import unicode_literals
from cloudant.document import Document
from django.core import exceptions
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from rest_framework.fields import empty
from .forms import signupform,loginform,npk,rev
from django.contrib import messages
import random
import csv
import requests
import matplotlib.pyplot as plt
from time import sleep

API_KEY = "hZYCe5CcFdL6-9Sjpps65riWv2ZXIyxZyDPqyKlaS02t"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
fields=['N','P','K','temperature','humidity','ph','rainfall']
link='https://us-south.ml.cloud.ibm.com/ml/v4/deployments/c58f94cf-d066-407b-a162-d8e2346d129c/predictions?version=2021-08-15'

Username = "5e76bd4d-d763-4fce-aff0-887cdde87a86-bluemix"
api = "3fFtXuIMXq4xEPtfCws-bggNAu9KCLxsmLALbWayfdMz"
client = Cloudant.iam(Username, api, connect=True)
client.connect()
session=client.session()
database=client['hack1']
db = Result(database.all_docs,include_docs=True)
def check(email,passw):
    i=0
    j=0
    while i==0:
        try:
            if email==db[j][0]["doc"]["email"] and passw==db[j][0]["doc"]["password"]:
                return True
            else:
                j=j+1
        except:
            i=1
    return False
def checkmail(email):
    i=0
    j=0
    while i==0:
        try:
            if email==db[j][0]["doc"]["email"]:
                return True
            else:
                j=j+1
        except:
            i=1
    return False
def updatemail(mail):
    for doc in database:
        if doc["email"]==mail:
            doc["log"]=1
            doc.save()
            break
def updatelogin(ip,mail):
    for doc in database:
        if doc["ip"]==ip and doc["email"]!=mail:
            doc["log"]=0
            doc.save()
        if doc["email"]==mail:
            doc["ip"]=ip
            doc["log"]=1
            doc.save()
def checklogin(ip):
    i="F"
    for doc in database:
        if doc["ip"]==ip and doc["log"]==1:
            i="P"
            return doc["name"]
    if i=="F":
        return "F"

def index(request):    
    return render(request, 'index.html')

def account(request):
    dict1={}
    ip = request.META.get('REMOTE_ADDR')
    for doc in database:
        if doc["ip"]==ip and doc["log"]==1:
            dict1['name']=doc["name"]
            dict1['mail']=doc["email"]
            dict1['district']=doc["district"]
            dict1['state']=doc["state"]
            dict1['sense']=doc["crop sense id"]
            dict1['crop']=doc["crop"]
            dict1['n']=doc["n"]
            dict1['p']=doc["p"]
            dict1['k']=doc["k"]
            dict1['ph']=doc["ph"]
            dict1["rainfall"]=doc["rainfall"]
            dict1["land"]=doc["land"]
    return render(request,'account.html',dict1)

def signin(request):
    if request.method == "POST":
        form1 = loginform(request.POST)
        if form1.is_valid():
            mail=str(form1.cleaned_data.get("email"))
            passw=str(form1.cleaned_data.get("password"))
            ip = request.META.get('REMOTE_ADDR')  
            if check(mail,passw) is True:
                updatelogin(ip,mail)
                return redirect('account')
            else:
                messages.error(request,'username or password not correct')
                return redirect('signin')
    else:    
        form1=loginform()
    return render(request,'login.html',{'forms':form1})

def signup(request):
    if request.method == "POST":
        form1 = signupform(request.POST)
        if form1.is_valid():
            name=str(form1.cleaned_data.get("name"))
            mail=str(form1.cleaned_data.get("email"))
            passw=str(form1.cleaned_data.get("password"))
            district=str(form1.cleaned_data.get("district"))
            state=str(form1.cleaned_data.get("state"))
            log=1
            x_forwarded_for = request.META.get('HTTPS_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            if ".com" in mail and "@" in mail:
                if checkmail(mail) is True:
                    messages.error(request,'Account Exists')
                    return redirect('signup')
                else:
                    jsonDocument = {
                                    "name": name,
                                    "email": mail,
                                    "password": passw,
                                    "district": district,
                                    "state": state,
                                    "ip":ip,
                                    "log":log,
                                    "crop sense id":"None",
                                    "crop":"None",
                                    "n":0,
                                    "p":0,
                                    "k":0,
                                    "ph":6,
                                    "rainfall":160,
                                    "land":10
                                    }
                    newDocument = database.create_document(jsonDocument)
                    return redirect('account')
            else:
                messages.error(request,'mail incorrect')
                return redirect('signup')
    else:
        form1=signupform()
    return render(request,'signup.html',{'forms':form1})

def logout(request):
    for doc in database:
        if doc["log"]==1:
            doc["log"]=0
            doc.save()   
    return redirect('index')

def edit(request):
    if request.method == "POST":
        form1 = npk(request.POST)
        if form1.is_valid():
            sense=str(form1.cleaned_data.get("crop sense id"))
            crop = str(form1.cleaned_data.get("crop"))
            n=str(form1.cleaned_data.get("n"))
            p=str(form1.cleaned_data.get("p"))
            k=str(form1.cleaned_data.get("k"))
            ph = str(form1.cleaned_data.get("ph"))
            rf = str(form1.cleaned_data.get("rainfall"))
            land = str(form1.cleaned_data.get("land"))
            for doc in database:
                if doc["log"]==1:
                    doc["crop"]=crop
                    doc["crop sense id"]=sense
                    doc["n"]=n
                    doc["p"]=p
                    doc["k"]=k
                    doc["ph"]=ph
                    doc["rainfall"]=rf
                    doc["land"]=land
                    doc.save()
            return redirect('account')
        else:
            messages.error(request,'mail incorrect')
            return redirect('edit')
    else:
        form1=npk()
    return render(request,'edit.html',{'forms':form1})

def predict(request):
    list1={}
    list1["temp"] = random.randint(25,38)
    list1["humidity"] = random.randint(60,80)
    path="staticfiles/images/revenue.csv"
    fi = open(path,mode='r')
    fil = csv.reader(fi,delimiter=',')
    for doc in database:
        if doc["log"]==1:
            list1["n"]=doc["n"]
            list1["p"]=doc["p"]
            list1["k"]=doc["k"]
            list1["ph"]=doc["ph"]
            list1["rainfall"]=doc["rainfall"]
            list1["land"]=doc["land"]
    if request.method == "POST":
        if '_pred' not in request.POST:
            form1 = rev(request.POST)
            if form1.is_valid():
                crop=str(form1.cleaned_data.get("cropchoice"))
                state=str(form1.cleaned_data.get("statechoice"))
                for row in fil:
                    if row[0] == crop and row[1] == state:          
                        list1['a']=row[2]
                        list1['b']=row[4]
                        list1['c']=row[5]
                        list1['d']=row[6]
                        break
                    if row[0] == crop:
                        list1['a']=row[2]
                        list1['b']=row[4]
                        list1['c']=row[5]
                        list1['d']=row[6]
                list1['forms']=form1
                return render(request,'predict.html',list1)
            else:
                return redirect('predict')
        else:
            field_values=[]
            for doc in database:
                if doc["log"]==1:
                    field_values.append(doc["n"])
                    field_values.append(doc["p"])
                    field_values.append(doc["k"])
                    field_values.append(list1["temp"])
                    field_values.append(list1["humidity"])
                    field_values.append(doc["ph"])
                    field_values.append(doc["rainfall"])
            payload_scoring = {"input_data": [{"fields":[fields], "values":[field_values]}]}
            #response_scoring = requests.post(link, json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
            list1["pred"]="Rice"
            list1["forms"]=rev()
            return render(request,'predict.html',list1)
    else:    
        form1=rev()
    list1["forms"]=form1
    return render(request,'predict.html',list1)

def terminal(request):
    x = [1,2,3,4,5,6,7,8,9,10]
    list1=[6.0,6.1,6.3,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7.0,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8.0]
    n = random.sample(range(80,90),10)
    p = random.sample(range(80,100),10)
    k = random.sample(range(70,90),10)
    ph = random.sample(list1,10)
    humidity = random.sample(range(60,90),10)
    temp = random.sample(range(25,35),10)
    x="""plt.plot(x,n)
    plt.savefig('staticfiles/images/n.jpg')
    plt.close()
    plt.plot(x,p)
    plt.savefig('staticfiles/images/p.jpg')
    plt.close()
    plt.plot(x,k)
    plt.savefig('staticfiles/images/k.jpg')
    plt.close()
    plt.plot(x,ph)
    plt.savefig('staticfiles/images/ph.jpg')
    plt.close()
    plt.plot(x,humidity)
    plt.savefig('staticfiles/images/humidity.jpg')
    plt.close()
    plt.plot(x,temp)
    plt.savefig('staticfiles/images/temp.jpg')
    plt.close()"""
    return render(request,'terminal.html')

def home(request):
    temp = random.randint(25,38)
    humidity = random.randint(40,60)
    rain = random.randint(10,90)
    name=[]
    crop=[]
    n=[]
    p=[]
    k=[]
    ph=[]
    for doc in database:
        if doc["log"]==1:
            nam = doc["name"]
            district=doc["district"]
            state=doc["state"]
    for doc in database:
        if doc["district"]==district and doc["state"]==state and doc["log"]==0:
            name.append(doc["name"])
            crop.append(doc["crop"])
            n.append(doc["n"])
            p.append(doc["p"])
            k.append(doc["k"])
            ph.append(doc["ph"])
    total=zip(name,crop,n,p,k,ph)
    return render(request,'home.html',{'nam':nam,'district':district,'temp':temp,'humidity':humidity,'rain':rain,'total':total})