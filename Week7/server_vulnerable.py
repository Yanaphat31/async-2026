import asyncio
from typing import Dict,List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

STUDENT_ID = {"6710301041", "6710301003", "6710301027", "6710301036", "6720301001", "6720301002"}
GROUP_SIZE = len(STUDENT_ID)
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1

coupon_db: List[str] = [f"COUPON-{i:02d}" for i in range(1, TOTAL_COUPONS + 1)]

current_coupon_index = 0

student_claims: Dict[str, List[str]] = {student_id: [] for student_id in STUDENT_ID}

class ClaimRequest(BaseModel):
    student_id: str

@app.post("/claim")

async def claim_coupon(request: ClaimRequest):
    global current_coupon_index
    student_id = request.student_id

    if student_id not in student_claims:
        return {"status": "INVALID_STUDENT", "message": "ไม่ทราบชื่อในระบบ"}

    if len(student_claims[student_id]) >= 2:
        return {"status": "LIMIT_REACHED", "message": "คุณรับคูปองครบ 2 ใบแล้ว"}

    #CRITICAL SECTION (no lock)
    if current_coupon_index < len(coupon_db):
        #1. อ่านค่า index ปัจจุบันของคูปองที่ยังไม่ได้ถูกอ้างสิทธิ์
        index_to_claim = current_coupon_index

        # หน่วงเวลาเปิดช่องให้ Race Condition เกิดขึ้นได้ง่ายขึ้น
        await asyncio.sleep(0.1)  # Simulate some processing delay

        #2.แจกคูปองตาม index ปัจจุบันให้กับนักเรียน
        coupon = coupon_db[index_to_claim]
        student_claims[student_id].append(coupon)

        #3. ขยับ index ปัจจุบันไปยังคูปองใบถัดไป
        current_coupon_index = index_to_claim + 1

        return {"status": "SUCCESS", "coupon": coupon, "total_owned": len(student_claims[student_id])}

    return {"status": "OUT_OF_COUPONS", "message": "คูปองหมดแล้ว"}

@app.get("/summary")
async def get_summary():
    return {"remaining_coupons": len(coupon_db) - current_coupon_index, 
            "student_claims": student_claims
        }