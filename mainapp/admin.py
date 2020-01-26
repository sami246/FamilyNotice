from django.contrib import admin
from .models import *

# Register your models here.

class ListAdmin(admin.ModelAdmin):
    list_display = ['nameOfList', 'get_tasks']

    def get_tasks(self, obj):
        return ", ".join([p.name for p in obj.task.all()])

class FamilyAdmin(admin.ModelAdmin):
    list_display = ['nameofFamily', 'CurrentMembers', 'CurrentLists']

    def CurrentMembers(self, obj):
        return ", ".join([p.user.username for p in obj.members.all()])

    def CurrentLists(self, obj):
        return ", ".join([p.nameOfList for p in obj.lists.all()])

admin.site.register(Family, FamilyAdmin)
admin.site.register(Member)
admin.site.register(List, ListAdmin)
admin.site.register(EventEntry)
admin.site.register(Task)
