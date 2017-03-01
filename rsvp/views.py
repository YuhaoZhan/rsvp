from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import  render_to_response  
from django.template import  RequestContext  
from django.http import HttpResponseRedirect  
from django.contrib.auth.models import User 
from django.contrib import auth  
from models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Create your views here.
def index(req):   
    username=req.session.get('username', '')  
    content = {'active_menu': 'homepage', 'user': username}  
    return render_to_response('index.html', content)
 
def regist(req):  
    if req.session.get('username', ''):  
         return HttpResponseRedirect('/rsvp/')  
    status=""  
    if req.POST:  
        username = req.POST.get("username","")  
        if User.objects.filter(username=username):  
            status = "user_exist"  
        else:  
            password=req.POST.get("password","")  
            repassword = req.POST.get("repassword","")  
            if password!=repassword:  
                status = "re_err"  
            else:  
                newuser=User.objects.create_user(username=username,password=password)  
                newuser.save()                               
                new_myuser = MyUser(user=newuser,email=req.POST.get("email"),name=username)      
                new_myuser.save()  
                status = "success"  
                return HttpResponseRedirect("/rsvp/login/")  
    return render(req,"regist.html",{"active_menu":"hompage","status":status,"user":""})  
  
def login(req):  
    if req.session.get('username', ''):  
        return HttpResponseRedirect('/rsvp/')  
    status=""  
    if req.POST:  
        username=req.POST.get("username","")  
        password=req.POST.get("password","")  
        user = auth.authenticate(username=username,password=password)   
        if user is not None:  
                auth.login(req,user)          
                req.session["username"]=username      
                return HttpResponseRedirect('/rsvp/')  
        else:  
            status="not_exist_or_passwd_err"  
    return render(req,"login.html",{"status":status})  

def logout(req):  
    auth.logout(req)  
    return HttpResponseRedirect('/rsvp/')  

def get_acad_list():  
    room_list = ConfeRoom.objects.all() 
    acad_list = set()  
    for room in room_list:  
        acad_list.add(room.acad)  
    return list(acad_list)  
  
 
def detail1(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","") 
    req.session["id"]=Id  
    if Id == "":  
        return HttpResponseRedirect('/rsvp/myevents/')  
    try:  
        event = Event.objects.get(pk=Id) 
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')   
    content = {"user":user,"event":event}  
    return render(req,'detail1.html',content)  

 
def get_order_list():  
    num_list=set()  
    order_list=Order.objects.all()  
    for order in order_list:  
        num_list.add(order.num)  
    return list(num_list)

def create_question(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = req.GET.get("id","") 
    req.session["id"]=Id  
    if Id == "":  
        return HttpResponseRedirect('/rsvp/myevents/')  
    if req.POST:
        question_text = req.POST.get("question_text","")
        event = Event.objects.get(pk=Id)
        q = TextQuestion(event=event,question_text=question_text)
        q.save()
        response_data = {}
        response_data['result'] = 'Create question successful'
        response_data['question_id'] = q.pk
        response_data['text'] = q.question_text
        response_data['author'] = username
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )


def viewroom(req):  
    username = req.session.get('username', '')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    acad_list=get_acad_list()   
    room_acad = req.GET.get("acad","all")                                           
    if room_acad not in acad_list:          
        room_acad = "all"  
        room_list=ConfeRoom.objects.all()  
    else:  
        room_list=ConfeRoom.objects.filter(acad=room_acad)  
    content = {"active_menu":'viewroom',"acad_list":acad_list,"room_acad":room_acad,"room_list":room_list,"user":user}  
    return render(req,'viewroom.html',content)

def edit(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","") 
    req.session["id"]=Id  
    if Id == "":  
        return HttpResponseRedirect('/rsvp/myevents/')  
    try:  
        event = Event.objects.get(pk=Id)
        owners = event.owners.all()
        vendors = event.vendors.all()
        guests = event.guests.all() 
        text_questions = event.textquestion_set.all()
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')   
    content = {"user":user,"event":event,"owners":owners,"vendors":vendors,"guests":guests,"text_questions":text_questions}  
    return render(req,'edit.html',content)  

#add a new user
@login_required
def add(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''
    Id = req.GET.get("id","") 
    req.session["id"]=Id 
    if Id=="":
        return HttpResponseRedirect('/rsvp/myevents/')
    status = ""
    event = Event.objects.get(pk=Id)
    if req.POST:
        name = req.POST.get("name","")
        pos = req.POST.get("type","")
        try:
            u = MyUser.objects.get(name=name)
        except MyUser.DoesNotExist:
            status="not_exist"  
            return render(req,"error.html",{"status":status})
        if pos == "owner":
            try:
                o = Owner.objects.get(user__name=name)
            except Owner.DoesNotExist:
                o = Owner(user=u)
                o.save()
            event.owners.add(o)
        if pos == "vendor":
            try:
                v = Vendor.objects.get(user__name=name)
            except Vendor.DoesNotExist:
                v = Vendor(user=u)
                v.save()
            event.vendors.add(v)
        if pos == "guest":
            try:
                g = Guest.objects.get(user__name=name)
            except Guest.DoesNotExist:
                g = Guest(user=u)
                g.save()
            event.guests.add(g)
        return HttpResponseRedirect("/rsvp/edit/?id="+Id)

    return render(req,"add.html",{})

@login_required
def create(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''
    if req.POST:
    	name = req.POST.get("eventname","")
    	time = req.POST.get("eventtime","")
    	event = Event(name=name, time=time)
    	event.save()
    	try:
    		o = Owner.objects.get(user=user)
    	except Owner.DoesNotExist:
    		o = Owner(user=user)
    		o.save()
    	event.owners.add(o)
    	return HttpResponseRedirect("/rsvp/myevents/")

    return render(req,"create.html",{})  

@login_required
def myevents(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    try:  
        owner_event = Event.objects.filter(owners__user__name=username)
        vendor_event = Event.objects.filter(vendors__user__name=username)
        guest_event = Event.objects.filter(guests__user__name=username)      
        us_sta = "no"  
        return render(req,"events.html",{"owner_event":owner_event,"vendor_event":vendor_event,"guest_event":guest_event,"us_sta":us_sta,"user":user})  
                  
    except:  
        us_sta = "yes"        
        return render(req,"events.html",{"us_sta":us_sta,"user":user})  
       
def cancel(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","")      
    room =Order.objects.get(pk=Id)  
    room.delete()  
    return render(req,"index.html") 

