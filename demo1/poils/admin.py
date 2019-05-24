from django.contrib import admin
from .models import Questions, Choices, MyUser
# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choices
    extra = 1

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','question']
    list_filter = ['question']
    search_fields = ['question']
    inlines = [ChoiceInline]

admin.site.register(Questions, QuestionsAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id','choice','num','cquesid']
    list_filter = ['choice']
    search_fields = ['choice']

admin.site.register(Choices, ChoiceAdmin)

admin.site.register(MyUser)