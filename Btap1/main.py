from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import EnrollmentCreate, EnrollmentResponse
from models import Enrollment
import Btap1.service as service
Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.post(
    "/enrollments",response_model=EnrollmentResponse,status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    enrollment: EnrollmentCreate,db: Session = Depends(get_db)
):
    student = service.get_student(db, enrollment.student_id)
    if not student:
        raise HTTPException(
            status_code=404,detail="Student not found"
        )
    course = service.get_course(db, enrollment.course_id)
    if not course:
        raise HTTPException(
            status_code=404,detail="Course not found"
        )
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,detail="Student is inactive"
        )
    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,detail="Course is closed"
        )
    duplicate = service.check_duplicate(
        db,enrollment.student_id,enrollment.course_id
    )
    if duplicate:
        raise HTTPException(
            status_code=400,detail="Student already enrolled"
        )
    total = service.count_enrollments(
        db,enrollment.course_id
    )
    if total >= course.max_students:
        raise HTTPException(
            status_code=400,detail="Course is full"
        )
    return service.create_enrollment(
        db,enrollment.student_id,enrollment.course_id
    )

@app.get("/students/{student_id}/courses")
def get_student_courses(
    student_id: int,db: Session = Depends(get_db)
):
    student = service.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=404,detail="Student not found"
        )
    enrollments = service.get_student_courses(
        db,student_id
    )
    courses = []
    for enrollment in enrollments:
        courses.append({
            "id": enrollment.course.id,"name": enrollment.course.name
        })
    return {
        "student_id": student.id,"full_name": student.full_name,"courses": courses
    }