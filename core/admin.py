from django.contrib import admin
from core.models import AdminUser,Student,StudentBase,FeedBack
from django.contrib.auth.admin import UserAdmin
# excel support 
from import_export.admin import ImportExportModelAdmin

@admin.register(AdminUser)
class CustomUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ['username', 'email', 'role', 'dept', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'dept')}),
    )
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        print(f'user id : {request.user.id}')
        if request.user.role == 'principal' : return qs 
        elif request.user.role == 'hod' :return qs.filter(dept=request.user.dept)
        return qs.filter(id=request.user.id)
    def has_add_permission(self, request):
        if hasattr(request.user, 'role') and request.user.role == 'staff':
            return False
        return super().has_add_permission(request)
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs 
        elif request.user.role == 'hod' or  request.user.role == 'staff' : return qs.filter(student__dept=request.user.dept)
        return qs 
@admin.register(StudentBase)
class StudentBaseAdmin(ImportExportModelAdmin):
     def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs 
        elif request.user.role == ('hod','staff') : return qs.filter(dept=request.user.dept)
        return qs      
@admin.register(FeedBack)
class FeedBackAdmin(ImportExportModelAdmin):
     def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs 
        elif request.user.role == 'hod': return qs.filter(dept=request.user.dept)
        elif request.user.role == 'staff' : return qs.filter(staff=request.user.staff)

        return qs 