from typing import List 
from ninja import Schema 
from pydantic import EmailStr


class AddHod(Schema):
    dept : str 
    email : EmailStr 
    password : str 


