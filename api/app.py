from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AWS PrivateLink Third-Party API",
    description="REST API exposed securely through AWS PrivateLink",
    version="1.0.0"
)


class Student(BaseModel):
    id: int
    name: str
    course: str
    attendance: int


students = [
    {
        "id": 1,
        "name": "Ponish",
        "course": "B.Tech",
        "attendance": 87
    },
    {
        "id": 2,
        "name": "Rahul",
        "course": "B.Tech",
        "attendance": 91
    }
]


@app.get("/")
def home():
    return {
        "message": "AWS PrivateLink API is running",
        "service": "Third-Party Student API",
        "status": "success"
    }


@app.get("/api/students")
def get_students():
    return students


@app.get("/api/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return {"error": "Student not found"}


@app.post("/api/students")
def create_student(student: Student):
    students.append(student.model_dump())

    return {
        "message": "Student created successfully",
        "student": student
    }


@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    return {"error": "Student not found"}
