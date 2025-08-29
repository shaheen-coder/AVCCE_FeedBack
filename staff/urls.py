from django.urls import path 
from staff.api import api
from staff import views 
urlpatterns = [
    path('api/',api.urls),
    # staf urls 
    path('',views.HODDash.as_view(),name='hod-dash'),
    # comman search 
    path('search/<str:mode>/<str:roa>/',views.Search.as_view(),name='hod-search'),
    path('analysis/mode/',views.AnalysisMode.as_view(),name='hod-ana-mode'),
    path('analysis/<str:mode>/<str:key>/<str:batch>/',views.Analysis.as_view(),name='hod-ana'),
    # analsysis dept
    path('analysis/<str:dept>/<str:batch>/',views.AnalysisDept.as_view(),name='hod-ana-dept'),
    path('analysis-mode/dept/',views.AnalysisDeptMode.as_view(),name='hod-ana-dept-mode'),
    # report url 
    path('student/report/search/<str:mode>/',views.StudentReportSearch.as_view(),name='hod-stu-search'),
    path('student/comt/<int:id>/<str:batch>/',views.StudentComment.as_view(),name='hod-stu-comt'),
    path('report/student/<int:id>/<str:batch>/',views.StudentReport.as_view(),name='hod-stu-report'),
    path('report/mode/',views.ReportMode.as_view(),name='hod-report-mode'),
    path('report/<str:mode>/<str:key>/<str:batch>/',views.Report.as_view(),name='hod-report'),
    path('report-dept/',views.DeptReportMode.as_view(),name='hod-report-dept-mode'),
    path('report/<str:dept>/<str:batch>/',views.DeptReport.as_view(),name='hod-dept-report'),
    path('ids/',views.StaffId.as_view(),name='staff-ids'),
    # add hod 
    path('add/staff/',views.AddHod.as_view(),name='hod-add-hod'),
    # ------------------------------------------------------------------------------------------------------
    # staff urls 
    path('teacher/',views.Staffdash.as_view(),name='tea-dash'),
    path('teacher/ana-mode/',views.StaffAnalysisMode.as_view(),name='tea-ana-mode'),
    path('teacher/report-mode/',views.StaffReportMode.as_view(),name='tea-report-mode'),
    path('teacher/analysis/<str:mode>/<int:id>/<str:batch>/',views.StaffAnalysis.as_view(),name='tea-ana'),
    path('teacher/report/<str:batch>/',views.StaffReport.as_view(),name='tea-report'),
    path('teacher/student/check/',views.StaffStudentCheck.as_view(),name='student-feed-status'),

]