from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout
# models import 
from core.models import Student
from staff.models import TimeScheduler
# other pkg 
from datetime import date,datetime

# home page view  
class Home(TemplateView):
    template_name = 'home.html'
class Team(TemplateView):
    template_name = 'developers.html'

#login page view 
class Login(View):
    template_name = 'login.html' 
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        regno = int(request.POST.get('regno'))
        dob = request.POST.get('dob')
        dob = datetime.strptime(dob,'%Y-%m-%d').date()
        try:
            student = Student.objects.get(student__regno=regno,student__dob=dob)
            time_scheduler = TimeScheduler.objects.filter(dept=student.student.dept).first()
            if not time_scheduler:
                return render(self.request,self.template_name,{"error": "No FeedBack found for the department."})
            current_time = date.today()
            if not (time_scheduler.start_time <= current_time <= time_scheduler.end_time):
                return render(self.request,self.template_name,{"error": "Feedback time is ended !!."})
            if (time_scheduler.feed == 1 and student.feed1_status) or (time_scheduler.feed == 2 and student.feed2_status):
                return render(self.request,self.template_name,{'error':"you have already sumited feedback"})
            
            # Check feed1_status and feed2_status
            if student.feed1_status and student.feed2_status:
                return render(self.request,self.template_name,{"error": "Student has already filled feedback forms."})

            # Determine which feedback is available
            available_feedback = 0
            if not student.feed1_status:
                available_feedback = 1 
            elif not student.feed2_status:
                available_feedback = 2 
            request.session['student_id'] = student.id
            request.session['student_feedno'] = available_feedback
            request.session['student_sec'] = student.section
            return redirect('feed-form',code='N')

        except Exception as error:
            print(f'error : {error}')
            return render(request,self.template_name,{'error' : 'student not found'})

# feedback form page 
class FeedForm(View):
    template_name = 'feed.html'
    def get(self,request,code):
        sid = request.session.get('student_id',None)
        student = Student.objects.get(id=sid)
        extra_course = False
        if student.semester > 4: 
            extra_course = True
        fid = 2 if student.feed1_status else 1 
        return render(request,self.template_name,{'fid':fid,'batch':student.student.batch,'extra_course':extra_course,'code':code})


# extra course chose page  
class CourseChocie(TemplateView):
    template_name = 'elective.html'

# seleted course subject list 
class CourseList(View):
    template_name = 'courseList.html'
    def get(self,request,cid):
        sid = request.session.get('student_id',None)
        student = Student.objects.get(id=sid)
        return render(request,self.template_name,{'student':student,'cid':cid})

def logout_view(request):
    logout(request)
    return redirect("admin:login")