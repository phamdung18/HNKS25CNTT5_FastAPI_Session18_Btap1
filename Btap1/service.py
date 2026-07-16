from sqlalchemy.orm import Session
from models import Student, Course, Enrollment

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def check_duplicate(db: Session, student_id: int, course_id: int):
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()
def count_enrollment(db: Session, course_id: int):
    return db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).count()
def create_enrollment(db: Session, student_id: int, course_id: int):
    enrollment = Enrollment(
        student_id=student_id,course_id=course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def get_student_courses(db: Session, student_id: int):
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()