from django.urls import path 
from hoc import views
from hoc.api import api
urlpatterns = [
    path('',views.HOCDash.as_view(),name='hoc-dash'),
    # comman search 
    path('search/<str:mode>/<str:roa>/',views.Search.as_view(),name='hoc-search'),
    path('analysis/mode/',views.AnalysisMode.as_view(),name='hoc-ana-mode'),
    path('analysis/<str:mode>/<str:key>/<str:batch>/',views.Analysis.as_view(),name='hoc-ana'),
    # analsysis dept
    path('analysis/<str:dept>/<str:batch>/',views.AnalysisDept.as_view(),name='hoc-ana-dept'),
    path('analysis-mode/dept/',views.AnalysisDeptMode.as_view(),name='hoc-ana-dept-mode'),
    # report url 
    path('student/report/search/<str:mode>/',views.StudentReportSearch.as_view(),name='hoc-stu-search'),
    path('student/comt/<int:id>/<str:batch>/',views.StudentComment.as_view(),name='hoc-stu-comt'),
    path('report/student/<int:id>/<str:batch>/',views.StudentReport.as_view(),name='hoc-stu-report'),
    path('report/mode/',views.ReportMode.as_view(),name='hoc-report-mode'),
    path('report/<str:mode>/<str:key>/<str:batch>/',views.Report.as_view(),name='hoc-report'),
    path('report-dept/',views.DeptReportMode.as_view(),name='hoc-report-dept-mode'),
    path('report/<str:dept>/<str:batch>/',views.DeptReport.as_view(),name='hoc-dept-report'),
    # add hod 
    path('add/hod/',views.AddHod.as_view(),name='hoc-add-hod'),

    path('api/',api.urls),
]