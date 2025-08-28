from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View 
# models
from staff.models import ClassStaff,Subject

# --------------------------------------------------------------------

# permisson view 

class IsHod(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'hod'
    def handle_no_permission(self):
        return render(self.request,'403.html', status=403)


class HODDash(IsHod,TemplateView):
    template_name = 'staff/dashboard.html'


class Search(IsHod,View):
    template1 = 'staff/search.html'
    def get(self,request,mode,roa):
        return render(request,self.template1,{'mode' : mode,'dept' : request.user.dept,'roa' : roa})


class AnalysisMode(IsHod,TemplateView):
    template_name = 'staff/analysis/analysis_mode.html'


class Analysis(IsHod,View):
    template = 'staff/analysis/analysis.html'
    def get(self,request,mode,key,batch):
        if mode == 'staff' : return render(request,self.template,{'mode':mode,'key' : int(key),'batch' : batch})
        elif mode == 'staffsub' : 
            staffd = ClassStaff.objects.get(id=int(key))
            return render(request,self.template,{'mode' : 'sub' ,'key' : staffd.staff.id, 'sub' : staffd.subject.code,'dept' : staffd.staff.dept ,'batch' : batch})
        elif mode == 'class' : 
            sem,sec,dept = key.split('-')
            return render(request,self.template,{'mode' : mode, 'key' : int(sem),'sec' : sec,'dept' :dept ,'batch' : batch})
        return render(request,self.template,{'error':'mode error '})

class AnalysisDeptMode(IsHod,TemplateView):
    template_name = 'staff/analysis/chosse_dept.html'
class AnalysisDept(IsHod,View):
    template = 'staff/analysis/analysis_dept.html'
    
    def get(self,request,dept,batch):
        return render(request,self.template,{'dept' : dept,'batch':batch})
# -------------------------------------------------------------------------------------------------

# report views 

class StudentReportSearch(IsHod,View):
    template_name = 'staff/report/ssearch.html'
    def get(self,request,mode):
        return render(request,self.template_name,{'mode' : mode})

class StudentReport(IsHod,View):
    template = 'staff/report/sreport.html'
    def get(self,request,id,batch):
        return render(request,self.template,{'id' : id,'batch' : batch})

class StudentComment(IsHod,View):
    template = 'staff/report/studentcomments.html'
    def get(self,request,id,batch):
        return render(request,self.template,{'id' : id, 'batch' : batch})
class ReportMode(IsHod,TemplateView):
    template_name = 'staff/report/report_mode.html'


class Report(IsHod,View):
    template = 'staff/report/report2.html'
    def get(self,request,mode,key,batch):
        if mode == 'staff' : return render(request,self.template,{'mode':mode,'key' : int(key),'batch' : batch})
        elif mode == 'staffsub' : 
            staffd = ClassStaff.objects.get(id=int(key))
            return render(request,self.template,{'mode' : mode,'key' : staffd.staff.id,'dept' : staffd.staff.dept, 'sub' : staffd.subject.code,'batch' : batch})
        elif mode == 'class' : 
            sem,sec,dept = key.split('-')
            return render(request,self.template,{'mode' : mode, 'key' : int(sem),'sec' : sec,'dept' :dept ,'batch' : batch})
        return render(request,self.template,{'error':'mode error '})

class DeptReportMode(IsHod,TemplateView):
    template_name = 'staff/report/choose_dept.html'

class DeptReport(IsHod,View):
    template = 'staff/report/dreport.html'
    def get(self,request,dept,batch):
        return render(request,self.template,{'dept' : dept,'batch' : batch})

class StaffId(IsHod,TemplateView):
    template_name = 'staff/staff_search.html'
# -------------------------------------------------------------------------------------------------

# upload hod 

class AddHod(IsHod,TemplateView):
    template_name = 'staff/addHod.html'


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
#                 staff views 
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


class IsStaff(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'staff'
    def handle_no_permission(self):
        return render(self.request,'403.html', status=403)

class Staffdash(IsStaff,TemplateView):
    template_name = 'teacher/dashboard.html'

class StaffAnalysisMode(IsStaff,TemplateView):
    template_name = 'teacher/analysis/analysis_mode.html'

class StaffReportMode(IsStaff,TemplateView):
    template_name = 'teacher/report/report_mode.html'

class StaffAnalysis(IsStaff,View):
    template = 'teacher/analysis/analysis.html'
    def get(self,request,mode,id,batch):
        return render(request,self.template,{'mode' : mode,'key' : id,'batch' : batch})

class StaffReport(IsStaff,View):
    template = 'teacher/report/report2.html'
    def get(self,request,batch):
        return render(request,self.template,{'batch' : batch})
    
class StaffStudentCheck(IsStaff,TemplateView):
    template_name = 'student_list.html'