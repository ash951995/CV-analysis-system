from app.models import Resume
from app import db
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_candidate(filename,text,structured_data):
    """ Save a candidate's information to the database """
    try:
        resume = Resume.query.filter_by(filename=filename).first()
        if resume:
            resume.data = structured_data
        else:
            resume = Resume(
        filename=filename,
        text_content=text,
        personal_info=structured_data.get("personalInfo", {}),
        education=structured_data.get("education", {}),
        work_experience=structured_data.get("workExperience", {}),
        skills=structured_data.get("skills", {}),
        projects=structured_data.get("projects", {}),
        certifications=structured_data.get("certifications", {})
    )
    
        db.session.add(resume)
        db.session.commit()
        logger.info(f"Successfully saved resume to database with ID: {resume.id}")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error storing CV data: {e}")
    