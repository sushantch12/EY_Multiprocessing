from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schema.assessment_schema import AssessmentCreate, AssessmentUpdate
from app.services.create_assessment_service import create_assessment, update_assessment, delete_assessment, get_assessment_by_id, list_assessments
from app.core.auth import get_current_user
from app.database.models import Users

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.post("/create", response_model=Assessments, status_code=201)
def create_assessment_endpoint(
    assessment_payload: str = Form(...), 
    current_user: Users = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Create an assessment by providing assessment details in JSON format.
    """
    return create_assessment(db=db, current_user=current_user, assessment_payload=assessment_payload)


@router.put("/update/{assessment_id}", response_model=Assessments, status_code=200)
def update_assessment_endpoint(
    assessment_id: int,
    assessment_payload: str = Form(...),
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing assessment by ID.
    """
    return update_assessment(db=db, assessment_id=assessment_id, current_user=current_user, assessment_payload=assessment_payload)


@router.delete("/delete/{assessment_id}", status_code=204)
def delete_assessment_endpoint(
    assessment_id: int, 
    current_user: Users = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Soft delete an assessment by ID.
    """
    return delete_assessment(db=db, assessment_id=assessment_id, current_user=current_user)


@router.get("/list", response_model=List[Assessments])
def list_assessments_endpoint(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    List all assessments with pagination.
    """
    return list_assessments(db=db, skip=skip, limit=limit)


@router.get("/{assessment_id}", response_model=Assessments)
def get_assessment_endpoint(
    assessment_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get a specific assessment by its ID.
    """
    return get_assessment_by_id(db=db, assessment_id=assessment_id)
