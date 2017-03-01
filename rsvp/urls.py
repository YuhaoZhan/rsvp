from django.conf.urls import url, include
from django.contrib import admin
from rsvp import views
admin.autodiscover()

urlpatterns = [
    url(r'^$',views.index),  
    url(r'^regist/$',views.regist),  
    url(r'^login/$',views.login),  
    url(r'^logout/$',views.logout),  
    url(r'^cancel/$',views.cancel),  
    url(r'^myevents/$',views.myevents),  
    url(r'^viewroom/$',views.viewroom),  
    url(r'^owner_event/$',views.detail1),
    url(r'^guest_event/$',views.detail3),
    url(r'^create/$',views.create),
    url(r'^edit/$',views.edit),
    url(r'^add/$',views.add),
    url(r'^create_question/$',views.create_question),
    url(r'^create_multi_choices_question/$',views.create_multi_choices_question),
    url(r'^can_view1/$',views.can_view1),
    url(r'^can_view2/$',views.can_view2),
]
