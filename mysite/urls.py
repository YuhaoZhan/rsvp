"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^rsvp/', include('rsvp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]


# from django.conf.urls import url, include
# from django.contrib import admin
# from rsvp import views
# admin.autodiscover()

# urlpatterns = [
# 	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#     url(r'^admin/', admin.site.urls),
#     url(r'^$',views.index),  
#     url(r'^regist/$',views.regist),  
#     url(r'^login/$',views.login),  
#     url(r'^logout/$',views.logout),  
#     url(r'^cancel/$',views.cancel),  
#     url(r'^events/$',views.myevents),  
#     url(r'^viewroom/$',views.viewroom),  
#     url(r'^owner_event/$',views.detail1),  
#     url(r'^events/create/$',views.create),
# ]
