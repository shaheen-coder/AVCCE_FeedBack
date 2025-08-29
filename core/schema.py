from ninja import Schema,ModelSchema
from typing import Optional, List , Dict
# models 
from staff.models import Subject,ClassStaff,Subject,Staff
from core.models import StudentBase
from core.models import Student as StudentModel

# student api 
class StudentSearchSchema(Schema):
    name: Optional[str] = None
    dept: str
    sec: Optional[str] = None
    sem: int
    batch : str 

class Student(ModelSchema):
    class Meta:
        model = StudentBase 
        fields = ['regno','name','dept']
class StudentOut(Schema):
   id : int 
   student : Student 
   section : str 
   semester : int  
# -------------------------------------------------------------------------------

# universal search schemas 

class StaffSchema(ModelSchema):
    class Meta:
        model = Staff
        fields = ['id','name','dept','gender']

class SubjectSchema(ModelSchema):
   class Meta:
        model= Subject 
        fields = ['name','code','semester','dept','course_type']

class ClassStaffSchema(Schema):
    id: int
    staff: StaffSchema
    subject: SubjectSchema
    section: str
    semester: int
    dept: str

class SearchParams(Schema):
    name: Optional[str] = None
    dept: Optional[str] = None
    gender: Optional[int] = None
    subject_code: Optional[str] = None
    section: Optional[str] = None
    semester: Optional[int] = None
    course_type: Optional[str] = None
    mode: Optional[str] = None


class StaffResponse(Schema):
    datas: List[StaffSchema]

class SubjectResponse(Schema):
    datas: List[SubjectSchema]

class ClassStaffResponse(Schema):
    datas: List[ClassStaffSchema]

class ErrorResponse(Schema):
    error: str

# ---------------------------------------------------------------------------
# class avalible section 

class ClassSearchParams(Schema):
    dept: str
    sem: Optional[int] = None

class ClassSearchResponse(Schema):
    dept: str
    sem: Optional[int]
    sections: List[str]
# --------------------------------------------------------
# feedback search     
class FeedSearchInput(Schema):
    id: int
    cid: int
    subid: Optional[str] = None

class FeedSearchOut(Schema):
    staff_id : int 
    staff_name : str
    subject_code : str 
    subject_name : str
    dept :str 
    semester : int 
# ----------------------------------------------------------------------

class BatchSchema(Schema):
    batch : List[str]

# -------------------------------------------------------------------------

class StudentStatusUpdateSchema(Schema):
    id : int 
    feedno : int 
# -------------------------------------------------------------------------

class FeedbackStudentStatusIN(Schema):
    sec :  str
    sem : int  
    dept : str 
    batch : str 

class FeedbackStudentStatusOut(ModelSchema):
    class Meta:
        model = StudentModel
        fields = "__all__"