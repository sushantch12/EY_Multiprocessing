from pydantic import BaseModel
from typing import List, Optional


class AssessmentContentBase(BaseModel):
    content_name: str
    content_type: str  # E.g., "PDF", "URL", etc.


class AssessmentCreate(BaseModel):
    content_name: str
    description: str
    content: List[AssessmentContentBase]


class AssessmentUpdate(BaseModel):
    content_name: str
    description: str
    content: List[AssessmentContentBase]


class Assessments(BaseModel):
    id: int
    content_name: str
    description: str
    created_by: int
    is_deleted: bool = False

    class Config:
        orm_mode = True
