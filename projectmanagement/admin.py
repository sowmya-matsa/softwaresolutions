from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Project, Task


# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "mobile", "type_of_user"]

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("mobile", "type_of_user")}),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'members','stage']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'about', 'project']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
