from ninja import NinjaAPI 
from pydantic import EmailStr
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings 

from hoc.schema import *

User = get_user_model()

api = NinjaAPI(
    title="HOC API",
    version="1.0.0",
    description="API for prinicpal ",
    urls_namespace="hoc-api",
)

@api.post("/hods/create/", response={201: List[EmailStr], 400: dict})
def create_hods(request, payload: List[AddHod]):
    """
    Create multiple HOD users and send them their passwords via email.
    Returns list of emails successfully created.
    """
    if not request.user.role == 'hoc':
        print(f'request user : {request.user.role} ')
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
            role='hod',
            dept=item.dept
        )
        user.is_staff = True
        user.is_superuser = True  
        user.save()
        created_emails.append(item.email)
    if errors:
        return 400, {"created": created_emails, "errors": errors}
    return 201, created_emails
