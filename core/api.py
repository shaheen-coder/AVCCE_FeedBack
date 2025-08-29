from ninja import NinjaAPI, Schema
from typing import Optional, List , Union
from ninja.errors import HttpError
from core.schema import *
#models 
from core.models import Student,FeedBack,StudentBase
from staff.models import Staff,ClassStaff,Subject
# django orm 
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from django.db import transaction

api = NinjaAPI(
    title="Core API",
    version="1.0.0",
    description="API for managing search data",
    urls_namespace="core-api",
    docs_url=None,
)
@api.post("/student-search/", response=List[StudentOut])
def student_search(request, data: StudentSearchSchema):
    filters = data.dict(exclude_none=True)
    if not filters:
        raise HttpError(400, "Please provide at least one search criterion.")
    if ('dept' not in filters) or ('batch' not in filters):
        raise HttpError(400, "The 'dept' and 'batch' field is required.")

    qs = Student.objects.select_related('student')
    # mandatory filter
    qs = qs.filter(student__dept=filters['dept'],student__batch=filters['batch'])
    qs = qs.filter(semester=filters['sem'])

    if 'name' in filters:
        qs = qs.filter(student__name__icontains=filters['name'])
    if 'sec' in filters:
        qs = qs.filter(section=filters['sec'])

    return qs

@api.post("/universal-search/", response={
    200: Union[StaffResponse, SubjectResponse, ClassStaffResponse, ErrorResponse]
})
def universal_search(request, params: SearchParams):
    """
    Universal search across Staff, Subject, and ClassStaff models.
    Supports multiple search parameters.
    """
    results = {}

    # Apply filters based on the mode
    if params.mode == 'staff':
        # Filter Staff model
        staff_queryset = Staff.objects.all()
        if params.name:
            staff_queryset = staff_queryset.filter(name__icontains=params.name)
        if params.dept:
            staff_queryset = staff_queryset.filter(dept=params.dept)
        if params.gender is not None:
            staff_queryset = staff_queryset.filter(gender=params.gender)
        
        # Optimize with select_related if needed in the future
        return {"datas": [StaffSchema.from_orm(staff) for staff in staff_queryset]}

    elif params.mode == 'sub':
        # Filter Subject model
        subject_queryset = Subject.objects.all()
        if params.subject_code:
            subject_queryset = subject_queryset.filter(code__icontains=params.subject_code)
        if params.dept:
            subject_queryset = subject_queryset.filter(dept=params.dept)
        if params.semester:
            subject_queryset = subject_queryset.filter(semester=params.semester)
        if params.course_type:
            course_type_filters = {
                "M": Q(course_type='M'),
                "E": Q(course_type='E'),
                "OE": Q(course_type='OE')
            }
            if params.course_type in course_type_filters:
                subject_queryset = subject_queryset.filter(course_type_filters[params.course_type])
        
        return {"datas": [SubjectSchema.from_orm(subject) for subject in subject_queryset]}

    elif params.mode == 'staffsub':
        # Filter ClassStaff model
        class_staff_queryset = ClassStaff.objects.all()
        if params.section:
            class_staff_queryset = class_staff_queryset.filter(section__iexact=params.section)
        if params.dept:
            class_staff_queryset = class_staff_queryset.filter(dept=params.dept)
        if params.semester:
            class_staff_queryset = class_staff_queryset.filter(semester=params.semester)
        if params.subject_code:
            class_staff_queryset = class_staff_queryset.filter(subject__code__icontains=params.subject_code)
        
        # Optimize with select_related for foreign keys
        class_staff_queryset = class_staff_queryset.select_related('staff', 'subject')
        
        return {"datas": [ClassStaffSchema.from_orm(cs) for cs in class_staff_queryset]}

    else:
        # Invalid mode
        return {"error": "Invalid mode specified."}


@api.post("/class-search/", response={200: ClassSearchResponse, 400: ErrorResponse})
def class_search(request, params: ClassSearchParams):
    """
    Search for available class sections by department and semester
    """
    dept = params.dept
    sem = params.sem
    
    if not dept:
        return 400, {"error": "department field missing"}
    
    queryset = ClassStaff.objects.filter(dept=dept)
    
    if sem is not None:
        queryset = queryset.filter(semester=sem)
    
    sections = queryset.values_list('section', flat=True).distinct()
    
    return {
        "dept": dept,
        "sem": sem,
        "sections": list(sections)
    }

@api.post("/feed/search/", response=List[FeedSearchOut])
def feed_search(request, payload: FeedSearchInput):
    student = get_object_or_404(Student, id=payload.id)

    if payload.subid and payload.subid != "null":
        queryset = ClassStaff.objects.filter(
            dept=student.student.dept,
            subject=payload.subid,
            section=student.section,
            semester=student.semester
        )
    else:
        def find_course_type(cid):
            if cid == 1 : return 'M'
            elif cid == 2 : return 'E'
            elif cid == 3 : return 'OE'
            else: return 'N'
        course_type = find_course_type(payload.cid)
        queryset = ClassStaff.objects.filter(
            dept=student.student.dept,
            semester=student.semester,
            section=student.section,
            subject__course_type=course_type
        )

    # If you wanted to return a 404 for “no results” in the single‑subject case:
    if payload.subid and not queryset.exists():
        return 404, {"error": "ClassStaff not found"}

    results = []
    for cs in queryset:
        results.append({
            "staff_id":     cs.staff.id,
            "staff_name":   cs.staff.name,
            "subject_code": cs.subject.code,
            "subject_name": cs.subject.name,
            "dept":         cs.dept,
            "semester":     cs.semester,
        })
    return results



@api.post('feed/status/',response={200 : Dict, 400 : ErrorResponse})
def feedstatusupdate(request, payload : StudentStatusUpdateSchema):
    student = Student.objects.get(id=payload.id)
    if payload.feedno == 1 : student.feed1_status = True
    elif payload.feedno == 2 : student.feed2_status = True
    student.save()
    return 200 , {'status' : 'status updated !! '}



@api.get('info/{student_id}/',response=StudentOut)
def student_info(request,student_id):
    return Student.objects.get(student=student_id)

@api.post("feedback/status/", response={200: list[FeedbackStudentStatusOut], 400: ErrorResponse})
def feedback_status(request, payload: FeedbackStudentStatusIN):
    data = Student.objects.filter(
        student__batch=payload.batch,
        student__dept=payload.dept,
        section=payload.sec,
    )
    if not data:
        return 400, {"error": "No student found"}
    return data
