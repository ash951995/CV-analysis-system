from app import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), index=True,  unique=True)
    text_content = db.Column(db.Text)
    personal_info = db.Column(db.JSON)
    education = db.Column(db.JSON)
    work_experience = db.Column(db.JSON)
    skills = db.Column(db.JSON) 
    projects = db.Column(db.JSON)
    certifications = db.Column(db.JSON)

    def __repr__(self):
        return f"<Resume {self.filename}>"