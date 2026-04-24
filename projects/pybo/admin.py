from django.contrib import admin

from .models import *

#https://docs.djangoproject.com/en/6.0/ref/contrib/admin/

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)