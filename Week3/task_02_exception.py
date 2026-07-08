# Objective: Extract returned data safely and inspect crashed tasks
# without breaking the main loop.

import asyncio
from time import ctime

# ฟังก์ชัน Worker สำหรับคำนวณผลหารแบบ Asynchronous
async def division_worker(a, b):
    await asyncio.sleep(0.5)  # จำลองการทำงานที่ใช้เวลา 0.5 วินาที
    return a / b  # คืนค่าผลหาร แ

async def main():
    # สร้าง Task ที่ทำงานสำเร็จ
    task_success = asyncio.create_task(division_worker(10, 2))

    # สร้าง Task ที่จะเกิดข้อผิดพลาดจากการหารด้วยศูนย์
    task_fail = asyncio.create_task(division_worker(10, 0))

    # รอให้ Task ทั้งสองมีเวลาประมวลผลจนเสร็จ
    await asyncio.sleep(1)
    
    # ตรวจสอบว่า Task สำเร็จ ทำงานเสร็จแล้ว และไม่มี Exception
    if task_success.done() and not task_success.exception():
        print(
            f"{ctime()} Task Success Result: {task_success.result()}"
        )  # ดึงและแสดงค่าผลลัพธ์อย่างปลอดภัย
        
    # ตรวจสอบว่า Task ที่ล้มเหลวทำงานเสร็จแล้ว
    if task_fail.done():
        print(
            f"{ctime()} Task Fail Exception: "
            f"{type(task_fail.exception()).__name__}"
        )  # ตรวจสอบและแสดงชื่อประเภทของ Exception ที่เกิดขึ้น

# เริ่มต้นรันโปรแกรม Asynchronous
asyncio.run(main())