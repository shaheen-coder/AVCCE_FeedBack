from django.contrib import admin
from staff.models import Staff,ClassStaff,Subject,TimeScheduler
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.



class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        import_id_fields = ['code']


@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs
        elif request.user.role == 'hod' : return qs.filter(dept=request.user.dept)
        elif request.user.role == 'staff': return qs.filter(id=request.user.staff.id)
        return qs
@admin.register(ClassStaff)
class ClassStaffAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs
        elif request.user.role == 'hod' : return qs.filter(dept=request.user.dept)
        elif request.user.role == 'staff': return qs.filter(staff=request.user.staff)
        return qs
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs
        elif request.user.role == ('hod','staff') : return qs.filter(dept=request.user.dept)
        return qs

@admin.register(TimeScheduler)
class TimeSchedulerAdmin(admin.ModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.role == 'hoc' : return qs
        elif request.user.role in ('hod','staff') : return qs.filter(dept=request.user.dept)
        return qs
