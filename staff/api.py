from ninja import NinjaAPI, Schema
from typing import Union, Dict
from staff.schema import *
# models
from django.db.models import Q
from staff.models import Staff, Subject, ClassStaff
from staff.metrics import * 
from core.models import FeedBack
# python 
from collections import defaultdict

from django.contrib.auth import get_user_model
api = NinjaAPI(
    title="Staff API",
    version="1.0.0",
    description="api for staff search and staff realated feedback data",
    urls_namespace="staff-api",
)


FEEDBACK_TERMS =[
        'Communication Skills of the Teacher',
        'Delivery of Lecture and Clarity in Teaching',
        'Ability of the Teacher to Explain a Particular Concept',
        'Audibility of Voice and legibility in Writing',
        'Innovative Teaching Aids',
        'Ability of the Teacher to respond to Difficulties Faced by Student on the Subject',
        'Availability and Approach of Teacher',
        'Review of University of Question Papers',
        'Relationship with student',
        'Subject Knowledge and Preparation'
    ]
@api.post("/analysis/", response={200: Dict, 400: ErrorResponse})
def analysis(request, params: AnalysisParams):
    """
    API for analysis of class, staff with subject and staff
    """
    global FEEDBACK_TERMS
    
    filter_conditions = {
        'class': Q(semester=params.key, section=params.sec, dept=params.dept,batch=params.batch),
        'sub': Q(staff=params.key,subject=params.sub,batch=params.batch),
        'staff': Q(staff=params.key, batch=params.batch),
    }
    
    if params.mode not in filter_conditions:
        return 400, {"error": "Invalid type specified"}
    
    feedback_entries = FeedBack.objects.filter(
        filter_conditions[params.mode]
    ).only('feed1', 'feed2')
    #print(f'debugger : {feedback_entries}')
    if not feedback_entries.exists():
        calculator = AnalysisCalculator()
        return calculator.compute_metrics([], FEEDBACK_TERMS)
    
    calculator = AnalysisCalculator()
    processed_data = []
    
    for entry in feedback_entries:
        # Process feed1
        if entry.feed1:
            processed_data.extend(calculator.process_feedback(entry.feed1))
        # Process feed2
        if entry.feed2:
            processed_data.extend(calculator.process_feedback(entry.feed2))
    
    return calculator.compute_metrics(processed_data, FEEDBACK_TERMS)

@api.get('/clg-analysis/',response={200:Dict,400: ErrorResponse})
def dept_analysis(request):
    # Simplified query to avoid select_related/only conflicts
    global FEEDBACK_TERMS
    feedbacks = FeedBack.objects.all()
    if not feedbacks.exists():
        return 400, "no feedback data found"
    
    calculator = DeptAnalysisCalculator()
    dept_data = defaultdict(list)
    
    for feedback in feedbacks:
        try:
            dept = feedback.dept
            # Process feed1
            if feedback.feed1:
                processed_feed1 = calculator.process_feedback(feedback.feed1)
                for item in processed_feed1:
                    item['dept'] = dept
                    dept_data[dept].append(item)
            
            # Process feed2
            if feedback.feed2:
                processed_feed2 = calculator.process_feedback(feedback.feed2)
                for item in processed_feed2:
                    item['dept'] = dept
                    dept_data[dept].append(item)
                    
        except AttributeError as e:
            print(f"Error processing feedback {feedback.id}: {str(e)}")
            continue
    
    results = {}
    for dept, data in dept_data.items():
        if data:  # Only process departments with data
            results[dept] = calculator.compute_metrics(data,FEEDBACK_TERMS)
    
    if not results:
        return 400, {"message": "No valid feedback data found"}
        
    return results
@api.post('/analysis/dept/',response={200 : Dict, 400 : ErrorResponse})
def analysis_dept(request, payload : AnalysisDeptParams):
    '''
        Analysis data generate by dept ! 
    '''
    global FEEDBACK_TERMS
    feedback_entries = FeedBack.objects.filter(dept=payload.dept,batch=payload.batch)
    if not feedback_entries.exists():
        calculator = AnalysisCalculator()
        return calculator.compute_metrics([], FEEDBACK_TERMS)
    
    calculator = AnalysisCalculator()
    processed_data = []
    
    for entry in feedback_entries:
        # Process feed1
        if entry.feed1:
            processed_data.extend(calculator.process_feedback(entry.feed1))
        # Process feed2
        if entry.feed2:
            processed_data.extend(calculator.process_feedback(entry.feed2))
    
    return calculator.compute_metrics(processed_data, FEEDBACK_TERMS)

# report api 
@api.post('/report/',response={200: Dict, 400 : ErrorResponse})
def report(request, params: ReportParams):
    """
    Generates feedback report by mode:
      - class:    by semester, section, dept
      - staff:    by staff_id, dept
      - sub: by staff_id, subject_id, dept
      - stu:      by student_id, dept

    Returns per-category + overall percentages and averages.
    """
    global FEEDBACK_TERMS
    # Normalize key for numeric lookups
    key = int(params.key) if params.mode in ("staff", "stu") else params.key

    # Define query filters based on mode
    filters_map = {
        "class":   Q(semester=params.sem, section=key, dept=params.dept,batch=params.batch),
        "staff":   Q(staff_id=key,batch=params.batch),
        "sub":Q(staff_id=key, subject_id=params.sub, dept=params.dept,batch=params.batch),
        "stu":     Q(student_id=key, dept=params.dept,batch=params.batch),
    }

    # Validate mode and required parameters
    if params.mode not in filters_map:
        return 400, "Invalid report type"
    if params.mode == "class" and params.sem is None:
        return 400, "Parameter 'sem' is required for class mode"
    if params.mode == "staffsub" and params.sub is None:
        return 400, "Parameter 'sub' is required for staffsub mode"

    # Stream only the JSON fields to minimize memory
    qs = FeedBack.objects.filter(filters_map[params.mode]).values_list('feed1', 'feed2')
    #print(f'debugger : {qs}')
    # One-pass accumulators
    cat_sums            = defaultdict(float)
    cat_counts          = defaultdict(int)
    cat_score_counts    = defaultdict(lambda: defaultdict(int))
    overall_sum         = 0.0
    overall_count       = 0
    overall_score_counts= defaultdict(int)

    for f1, f2 in qs.iterator():
        for feed in (f1, f2):
            if not isinstance(feed, dict):
                continue
            for cat, val in feed.items():
                if isinstance(val, (int, float)):
                    # per-category
                    cat_sums[cat] += val
                    cat_counts[cat] += 1
                    cat_score_counts[cat][val] += 1
                    # overall
                    overall_sum += val
                    overall_count += 1
                    overall_score_counts[val] += 1

    # If no feedback found
    if overall_count == 0:
        return {"data": {}, "terms": FEEDBACK_TERMS}

    # Build per-category metrics
    result: Dict[str, Dict[str, float]] = {}
    for cat, count in cat_counts.items():
        scores = cat_score_counts[cat]
        result[cat] = {
            "percentage_5s": round(scores.get(5, 0) / count * 100, 2),
            "percentage_3s": round(scores.get(3, 0) / count * 100, 2),
            "percentage_1s": round(scores.get(1, 0) / count * 100, 2),
            "average":       round(cat_sums[cat] / count, 2),
        }

    # Build overall metrics
    result["overall"] = {
        "percentage_5s": round(overall_score_counts.get(5, 0) / overall_count * 100, 2),
        "percentage_3s": round(overall_score_counts.get(3, 0) / overall_count * 100, 2),
        "percentage_1s": round(overall_score_counts.get(1, 0) / overall_count * 100, 2),
        "average":       round(overall_sum / overall_count, 2),
    }

    return {"data": result, "terms": FEEDBACK_TERMS}

# helper func 
def _compute_simple_metrics(scores: list) -> Dict[str, float]:
        """Compute 5s/3s/1s percentages and average."""
        total = len(scores)
        counts = defaultdict(int)
        ssum = 0.0
        for v in scores:
            counts[v] += 1
            ssum += v
        return {
            '5s':  round(counts.get(5, 0) / total * 100, 2),
            '3s':  round(counts.get(3, 0) / total * 100, 2),
            '1s':  round(counts.get(1, 0) / total * 100, 2),
            'avg': round(ssum / total, 2)
        }

@api.post('student/report/',response={200 : Dict, 400 : ErrorResponse})
def student_report(request, params: StudentParams):
    """Feedback metrics grouped by subject for a given student."""
    
    qs = FeedBack.objects.filter(student_id=params.student_id,batch=params.batch) \
                     .values_list('subject__code', 'feed1', 'feed2')

    subj_scores = defaultdict(list)
    total_scores = []

    for subj_code, f1, f2 in qs.iterator():
        for feed in (f1, f2):
            if isinstance(feed, dict):
                for val in feed.values():
                    if isinstance(val, (int, float)):
                        subj_scores[subj_code].append(val)
                        total_scores.append(val)

    if not total_scores:
        return 400, "No feedback data available for this student"

    # Compute per-subject and overall metrics
    result = {
        subj: _compute_simple_metrics(scores)
        for subj, scores in subj_scores.items()
    }
    result['overall'] = _compute_simple_metrics(total_scores)

    return result

@api.get('institution/report/{batch}',response={200 : Dict, 400 : ErrorResponse})
def institution_report(request,batch):
    """Feedback metrics grouped by department across all feedback."""
    
    
    qs = FeedBack.objects.filter(batch=batch).select_related('staff') \
                     .values_list('staff__dept', 'feed1', 'feed2')

    dept_scores = defaultdict(list)
    total_scores = []

    for dept, f1, f2 in qs.iterator():
        for feed in (f1, f2):
            if isinstance(feed, dict):
                for val in feed.values():
                    if isinstance(val, (int, float)):
                        dept_scores[dept].append(val)
                        total_scores.append(val)

    if not total_scores:
        raise HttpError(404, "No feedback data available")

    result = {
        dept: _compute_simple_metrics(scores)
        for dept, scores in dept_scores.items()
    }
    result['overall'] = _compute_simple_metrics(total_scores)

    return result

@api.post('dept/report/',response={200 : Dict, 400 : ErrorResponse})
def department_report(request,payload : DeptParams):
    """Feedback metrics grouped by staff member for a given department."""
    qs = FeedBack.objects.filter(staff__dept=payload.dept,batch=payload.batch) \
                     .values_list('staff__name', 'feed1', 'feed2')

    staff_scores = defaultdict(list)
    total_scores = []

    for staff_name, f1, f2 in qs.iterator():
        for feed in (f1, f2):
            if isinstance(feed, dict):
                for val in feed.values():
                    if isinstance(val, (int, float)):
                        staff_scores[staff_name].append(val)
                        total_scores.append(val)

    if not total_scores:
        raise HttpError(404, "No feedback data available for this department")

    result = {
        name: _compute_simple_metrics(scores)
        for name, scores in staff_scores.items()
    }
    result['overall'] = _compute_simple_metrics(total_scores)

    return result

@api.get('student/comments/{student_id}/{batch}',response={200 : List[CommentOut], 400 : ErrorResponse})
def comment_report(request, student_id: int,batch :str):
    """Retrieve comments (msg, subject name/code) for a given student."""
    qs = FeedBack.objects.filter(student_id=student_id,batch=batch) \
                     .values_list('msg', 'subject__name', 'subject__code')

    comments = [
        {"msg": msg, "subject_name": name, "subject_code": code}
        for msg, name, code in qs
    ]
    if not comments:
        raise HttpError(404, "No feedback found for this student.")
    return comments

@api.get('get/batch/', response={200: Dict})
def get_batch(request):
    unique_batches = list(FeedBack.objects.values_list('batch', flat=True).distinct())
    return {'batch': unique_batches}



# ------------------------------------------------------------------------------------------------------- 

# staff info api 
@api.get('info/staff/{staff_id}/',response=StaffInfo)
def staff_info(request,staff_id):
    return Staff.objects.get(id=staff_id)


# staff with sub info api 
@api.get('info/sub/{staffsub_id}/',response=StaffSubInfo)
def staffsub_info(request,staffsub_id):
    return ClassStaff.objects.get(id=staffsub_id)


# ------------------------------------------------------
# adding staff 

@api.post("/create/", response={201: List[EmailStr], 400: dict})
def create_staff(request, payload: List[AddStaff]):
    """
    Create multiple STAFF user and send them their passwords via email.
    Returns list of emails successfully created.
    """
    User = get_user_model()
    if not request.user.role in ('hod','hoc'):
        return 400, {'error' : 'access deined !!'}
    created_emails = []
    errors = []

    for item in payload:
        # Check if user with this email already exists
        if User.objects.filter(email=item.email).exists():
            errors.append({"email": item.email, "error": "User already exists"})
            continue

        # Create user
        user = User.objects.create_user(
            username=item.email,
            email=item.email,
            password=item.password,
            role='staff',
            dept=item.dept,
            staff_id=item.staff_id
        )
        user.is_staff = True
        user.is_superuser = True  
        user.save()
        created_emails.append(item.email)
    if errors:
        return 400, {"created": created_emails, "errors": errors}
    return 201, created_emails
