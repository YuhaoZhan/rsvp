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

@login_required
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
        guests = event.guests.all()
        text_questions = event.textquestion_set.all()
        ''' each array is a response set'''
        text_responses = []
        choice_questions = event.choicequestion_set.all()
        choice_responses = []
        index = 0
        for guest in guests:
            text_responses.append([])
            choice_responses.append([])
            for text_question in text_questions:
                text_responses[index].append(text_question.textresponse_set.filter(username=guest.user.name))
            
            for choice_question in choice_questions:
                choice_responses[index].append(choice_question.choice_set.filter(choiceresponse__username=guest.user.name))
            index += 1
            
        zipped_text_responses = zip(guests, text_responses)
        zipped_choice_responses = zip(guests, choice_responses)
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')
    content = {"user":user,"event":event, "text_questions":text_questions, "zipped_text_responses":zipped_text_responses, "choice_questions":choice_questions, "zipped_choice_responses":zipped_choice_responses}  
    return render(req,'detail1.html',content)  

@login_required
def detail2(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","")
    req.session["id"]=Id

    try:  
        event = Event.objects.get(pk=Id)
        guests = event.guests.all()
        choice_questions = event.choicequestion_set.filter(vendors__user__name=username)
        text_questions = event.textquestion_set.filter(vendors__user__name=username)
        text_responses = []
        choice_responses = []
        index = 0
        for guest in guests:
            text_responses.append([])
            choice_responses.append([])
            for text_question in text_questions:
                ts = text_question.textresponse_set.filter(username=guest.user.name)
                if ts.count() > 0:
                    text_responses[index].append(ts.first())
                else:
                    tmp = TextResponse(question=text_question,response_text="Not answered yet.",username=guests.user.name)
                    tmp.save()
                    text_responses[index].append(tmp)
            
            for choice_question in choice_questions:
                cs = choice_question.choice_set.filter(choiceresponse__username=guest.user.name)
                if cs.count() > 0:
                    choice_responses[index].append(cs)
                else:    
                    choice_responses[index].append(choice_question.choice_set.all())
                
            index += 1
            
        zipped_text_responses = zip(guests, text_responses)
        zipped_choice_responses = zip(guests, choice_responses)
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')    
    content = {"user":user,"event":event, "text_questions":text_questions, "zipped_text_responses":zipped_text_responses, "choice_questions":choice_questions, "zipped_choice_responses":zipped_choice_responses}  
    return render(req,'detail2.html',content)


@login_required
def detail3(req):
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
        text_questions = event.textquestion_set.all()
        text_responses = []
        choice_questions = event.choicequestion_set.all()
        choice_responses = []

        for text_question in text_questions:
            ts = text_question.textresponse_set.filter(username=username)
            if ts.count() > 0:
                text_responses.append(ts.first())
            else:
                tmp = TextResponse(question=text_question,response_text="Not answered yet.",username=username)
                tmp.save()
                text_responses.append(tmp)
        
        for choice_question in choice_questions:
            cs = choice_question.choice_set.filter(choiceresponse__username=username)
            if cs.count() > 0:
                choice_responses.append(cs)
            else:    
                choice_responses.append(choice_question.choice_set.all())
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')   
    content = {"user":user,"event":event,"text_questions":text_questions,"text_responses":text_responses,"choice_questions":choice_questions,"choice_responses":choice_responses}  
    return render(req,'detail3.html',content)


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
        vendors = event.vendors.all()
        vendorList = []
        for vendor in vendors:
            vendorList.append(vendor.user.name)
        q = TextQuestion(event=event,question_text=question_text)
        q.save()
        response_data = {}
        response_data['result'] = 'Create question successful'
        response_data['question_id'] = q.pk
        response_data['text'] = q.question_text
        response_data['author'] = username
        response_data['vendors'] = vendorList
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def create_multi_choices_question(req):
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
        choices = req.POST.getlist('choices[]')
        event = Event.objects.get(pk=Id)
        vendors = event.vendors.all()
        q = ChoiceQuestion(event=event,question_text=question_text)
        q.save()
        for c_text in choices:
            c = Choice(question=q,choice_text=c_text)
            c.save()
        vendorList = []
        for vendor in vendors:
            vendorList.append(vendor.user.name)
        response_data = {}
        response_data['result'] = 'Create question successful'
        response_data['choices'] = choices
        response_data['text'] = q.question_text
        response_data['author'] = username
        response_data['vendors'] = vendorList
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def can_view1(req):
    if req.POST:
        tq_id = req.POST.get("tq_id","")
        tq = TextQuestion.objects.get(pk=tq_id)
        vendor_name = req.POST.get("vendor_name","")
        vendor = Vendor.objects.get(user__name=vendor_name)
        tq.vendors.add(vendor)
        tq.save()
        response_data = {}
        response_data['result'] = 'vendor can view successful'
        response_data['text'] = tq.question_text
        response_data['vendors'] = vendor_name
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def can_view2(req):
    if req.POST:
        cq_id = req.POST.get("cq_id","")
        cq = ChoiceQuestion.objects.get(pk=cq_id)
        vendor_name = req.POST.get("vendor_name","")
        vendor = Vendor.objects.get(user__name=vendor_name)
        cq.vendors.add(vendor)
        cq.save()
        response_data = {}
        response_data['result'] = 'vendor can view successful'
        response_data['text'] = cq.question_text
        response_data['vendors'] = vendor_name
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def save1(req):
    if req.POST:
        tr_id = req.POST.get("tr_id","")
        tr = TextResponse.objects.get(pk=tr_id)
        new_answer = req.POST.get("new_answer","")
        tr.response_text = new_answer
        tr.save()
        response_data = {}
        response_data['result'] = 'vendor can view successful'
        response_data['text'] = new_answer
        response_data['tr_id'] = tr.id
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def save2(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    if req.POST:
        cq_id = req.POST.get("cq_id","")
        cq = ChoiceQuestion.objects.get(pk=cq_id)
        new_answer = req.POST.get("new_answer","")
        query_set = cq.choice_set.filter(choiceresponse__username=username)
        if query_set.count()>0:
            old_choice = query_set.first()
            old_response = old_choice.choiceresponse_set.filter(username=username)
            old_response.first().delete()
            new_choice = Choice.objects.filter(choice_text=new_answer)
            new_response = ChoiceResponse(user_choice = new_choice.first(), username=username)
            new_response.save()
        else:
            new_choice = Choice.objects.filter(choice_text=new_answer).first()
            new_response = ChoiceResponse(user_choice = new_choice,username=username)
            new_response.save()
        response_data = {}
        response_data['result'] = 'save choice response successful'
        response_data['text'] = new_choice.choice_text
        response_data['cq_id'] = cq.id
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )


def finalize1(req):
    if req.POST:
        tq_id = req.POST.get("tq_id","")
        tq = TextQuestion.objects.get(pk=tq_id)
        tq.finalized = True
        tq.save()
        response_data = {}
        response_data['result'] = 'finalize successful'
        response_data['tq_id'] = tq.id
        response_data['finalized'] = tq.finalized
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

def finalize2(req):
    if req.POST:
        cq_id = req.POST.get("cq_id","")
        cq = ChoiceQuestion.objects.get(pk=cq_id)
        cq.finalized = True
        cq.save()
        response_data = {}
        response_data['result'] = 'finalize successful'
        response_data['cq_id'] = cq.id
        response_data['finalized'] = cq.finalized
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
        choice_questions = event.choicequestion_set.all()
    except:               
        return HttpResponseRedirect('/rsvp/myevents/')   
    content = {"user":user,"event":event,"owners":owners,"vendors":vendors,"guests":guests,"text_questions":text_questions,"choice_questions":choice_questions}  
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
        permission = req.POST.get("plusone","")
    	event = Event(name=name, time=time)
        if permission == "Yes":
            event.plusone = True
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

