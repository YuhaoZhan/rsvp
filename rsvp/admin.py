from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(MyUser)
admin.site.register(Owner)
admin.site.register(Vendor)
admin.site.register(Guest)
admin.site.register(Event)
admin.site.register(ChoiceQuestion)
admin.site.register(Choice)
admin.site.register(ChoiceResponse)
admin.site.register(TextQuestion)
admin.site.register(TextResponse)
