from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View 
# models
from staff.models import ClassStaff,Subject

# --------------------------------------------------------------------

# permisson view 

class IsPrincipal(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'hoc'
    def handle_no_permission(self):
        return render(self.request,'403.html', status=403)


class HOCDash(IsPrincipal,TemplateView):
    template_name = 'hoc/dashboard.html'


class Search(IsPrincipal,View):
    template1 = 'hoc/search.html'
    def get(self,request,mode,roa):
        return render(request,self.template1,{'mode' : mode,'roa' : roa})


class AnalysisMode(IsPrincipal,TemplateView):
    template_name = 'hoc/analysis/analysis_mode.html'


class Analysis(IsPrincipal,View):
    template = 'hoc/analysis/analysis.html'
    def get(self,request,mode,key,batch):
        if mode == 'staff' : return render(request,self.template,{'mode':mode,'key' : int(key),'batch' : batch})
        elif mode == 'staffsub' : 
            staffd = ClassStaff.objects.get(id=int(key))
            return render(request,self.template,{'mode' : 'sub','key' : staffd.staff.id, 'sub' : staffd.subject.code,'dept' : staffd.staff.dept ,'batch' : batch})
        elif mode == 'class' : 
            sem,sec,dept = key.split('-')
            return render(request,self.template,{'mode' : mode, 'key' : int(sem),'sec' : sec,'dept' :dept ,'batch' : batch})
        return render(request,self.template,{'error':'mode error '})

class AnalysisDeptMode(IsPrincipal,TemplateView):
    template_name = 'hoc/analysis/chosse_dept.html'
class AnalysisDept(IsPrincipal,View):
    template = 'hoc/analysis/analysis_dept.html'
    
    def get(self,request,dept,batch):
        return render(request,self.template,{'dept' : dept,'batch':batch})
# -------------------------------------------------------------------------------------------------

# report views 

class StudentReportSearch(IsPrincipal,View):
    template_name = 'hoc/report/ssearch.html'
    def get(self,request,mode):
        return render(request,self.template_name,{'mode' : mode})

class ReportMode(IsPrincipal,TemplateView):
    template_name = 'hoc/report/report_mode.html'


class Report(IsPrincipal,View):
    template = 'hoc/report/report2.html'
    def get(self,request,mode,key,batch):
        if mode == 'staff' : return render(request,self.template,{'mode':mode,'key' : int(key),'batch' : batch})
        elif mode == 'staffsub' : 
            staffd = ClassStaff.objects.get(id=int(key))
            return render(request,self.template,{'mode' : mode,'key' : staffd.staff.id,'dept' : staffd.staff.dept, 'sub' : staffd.subject.code,'batch' : batch})
        elif mode == 'class' : 
            sem,sec,dept = key.split('-')
            return render(request,self.template,{'mode' : mode, 'key' : int(sem),'sec' : sec,'dept' :dept ,'batch' : batch})
        return render(request,self.template,{'error':'mode error '})

class StudentReport(IsPrincipal,View):
    template = 'hoc/report/sreport.html'
    def get(self,request,id,batch):
        return render(request,self.template,{'id' : id,'batch' : batch})

class StudentComment(IsPrincipal,View):
    template = 'hoc/report/studentcomments.html'
    def get(self,request,id,batch):
        return render(request,self.template,{'id' : id, 'batch' : batch})
class DeptReportMode(IsPrincipal,TemplateView):
    template_name = 'hoc/report/choose_dept.html'

class DeptReport(IsPrincipal,View):
    template = 'hoc/report/dreport.html'
    def get(self,request,dept,batch):
        return render(request,self.template,{'dept' : dept,'batch' : batch})

# -------------------------------------------------------------------------------------------------

# upload hod 

class AddHod(IsPrincipal,TemplateView):
    template_name = 'hoc/addHod.html'
