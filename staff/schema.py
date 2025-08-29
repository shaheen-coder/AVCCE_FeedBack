from ninja import Schema, ModelSchema
from typing import Optional, List ,Any
from pydantic import EmailStr
from staff.models import Staff,Subject

# analysis Schema 
class AnalysisParams(Schema):
    mode: str  
    key: Any
    sub : Optional[str] = None 
    sec : Optional[str] = None   
    dept: Optional[str] = None  
    batch : str

class ErrorResponse(Schema):
    error: str

class AnalysisDeptParams(Schema):
    dept : str 
    batch : str
# ------------------------------------------------------------------------

# report schema 

class ReportParams(Schema):
    mode: str                   
    key: Any                    
    sem: Optional[int] = None   
    sub: Optional[Any] = None   
    dept : Optional[str] = None                     
    batch : str 
# ------------------------------------------------------------------------
# student 
class StudentParams(Schema):
    student_id: int
    batch : str 
# ------------------------------------------------------------------------
# dept 
class DeptParams(Schema):
    dept: str
    batch : str 

# -----------------------------------------------------------------------

class CommentOut(Schema):
    msg : str 
    subject_name : str 
    subject_code : str
# -------------------------------------------------------------------------

class BatchSchema(Schema):
    batch : List[str]


# ---------------------------------------------------------------------------

class StaffInfo(ModelSchema):
    class Meta:
        model = Staff 
        fields = ['id','name','dept','gender']

class SubjectInfo(ModelSchema):
    class Meta:
        model = Subject 
        fields = ['code','name']
class StaffSubInfo(Schema):
    id : int 
    staff : StaffInfo
    subject : SubjectInfo 


class AddStaff(Schema):
    email : EmailStr
    password : str 
    dept : str 
    staff_id : int 