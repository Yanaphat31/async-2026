import asyncio
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

STUDENTS = [
    "Student_01",
    "Student_02",
    "Student_03",
    "Student_04",
    "Student_05"
]

GROUP_SIZE = len(STUDENTS)
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1

coupons_db: List[str] = [
    f"COUPON-{i:02d}" for i in range(1, TOTAL_COUPONS + 1)
]

current_coupon_index = 0

student_claims: Dict[str, List[str]] = {
    student_id: [] for student_id in STUDENTS
}

# 1. ประกาศสร้าง Mutex Lock สำหรับควบคุมการเข้าถึงข้อมูลร่วม
coupon_lock = asyncio.Lock()


class ClaimRequest(BaseModel):
    student_id: str


@app.post("/claim")
async def claim_coupon(req: ClaimRequest):

    global current_coupon_index

    student_id = req.student_id

    # 2. ใช้ async with coupon_lock ครอบ Critical Section ทั้งหมด
    async with coupon_lock:

        if student_id not in student_claims:
            return {
                "status": "INVALID_STUDENT",
                "message": "ไม่พบรายชื่อในระบบ"
            }