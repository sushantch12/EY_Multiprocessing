from sqlalchemy.orm import Session
from app.database.models import Assessments, AssessmentContent, Users
from app.schema.assessment_schema import AssessmentCreate, AssessmentUpdate
from app.core.exceptions import NotFoundException


def create_assessment(db: Session, current_user: Users, assessment_payload: str):
    # Parse the assessment_payload (which should be in JSON format)
    assessment_data = AssessmentCreate.parse_raw(assessment_payload)
    
    # Create the assessment record
    assessment = Assessments(
        content_name=assessment_data.content_name,
        description=assessment_data.description,
        created_by=current_user.id,
        # Add any other necessary fields
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    # Handle assessment content if any exists
    for content in assessment_data.content:
        assessment_content = AssessmentContent(
            assessment_id=assessment.id,
            content_name=content.content_name,
            content_type=content.content_type,
        )
        db.add(assessment_content)
    
    db.commit()
    return assessment


def update_assessment(db: Session, assessment_id: int, current_user: Users, assessment_payload: str):
    assessment_data = AssessmentUpdate.parse_raw(assessment_payload)
    
    # Retrieve the existing assessment
    assessment = db.query(Assessments).filter(Assessments.id == assessment_id).first()
    if not assessment:
        raise NotFoundException("Assessment not found")

    assessment.content_name = assessment_data.content_name
    assessment.description = assessment_data.description
    # Update other fields as needed

    db.commit()
    db.refresh(assessment)
    
    # Update the assessment content if needed
    for content in assessment_data.content:
        # Assuming content is linked with assessment in the payload
        assessment_content = AssessmentContent(
            assessment_id=assessment.id,
            content_name=content.content_name,
            content_type=content.content_type,
        )
        db.add(assessment_content)

    db.commit()
    return assessment


def delete_assessment(db: Session, assessment_id: int, current_user: Users):
    # Retrieve the assessment to soft delete
    assessment = db.query(Assessments).filter(Assessments.id == assessment_id).first()
    if not assessment:
        raise NotFoundException("Assessment not found")
    
    # Soft delete logic (mark as deleted or any other flag)
    assessment.is_deleted = True
    db.commit()
    return {"message": "Assessment deleted successfully"}


def get_assessment_by_id(db: Session, assessment_id: int):
    assessment = db.query(Assessments).filter(Assessments.id == assessment_id).first()
    if not assessment:
        raise NotFoundException("Assessment not found")
    return assessment


def list_assessments(db: Session, skip: int = 0, limit: int = 10):
    assessments = db.query(Assessments).offset(skip).limit(limit).all()
    return assessments

