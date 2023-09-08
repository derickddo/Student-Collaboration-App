from django.contrib import admin
from .models import CustomUser, Group, Task, GroupMessage, TaskFile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(GroupMessage)
admin.site.register(TaskFile)