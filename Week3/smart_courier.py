# Delivery System): นักศึกษาต้องเขียน try...except CancelledError ได้ถูกต้อง 
# และใช้ .get_name(), .cancel(), และ .cancelled() ได้
# smart_courier.py
# Assignment 1: Smart Courier System (40 คะแนน)


import asyncio
from time import ctime

async def delivery_task(package_id: str, duration: float):
    """
    จำลองการส่งพัสดุ ใช้เวลา `duration` วินาที
    ถ้าถูกยกเลิกระหว่างทาง (CancelledError) ให้พิมพ์ข้อความแล้ว re-raise
    เพื่อให้ task จบสถานะเป็น cancelled จริง ๆ
    """
    print(f"[{ctime()}] Courier started delivering {package_id}...")
    try:
        await asyncio.sleep(duration)
        print(f"[{ctime()}] Package {package_id} Delivered!")
        return f"Package {package_id} Delivered!"
    except asyncio.CancelledError:
        print(f"[{ctime()}] Delivery Canceled! Returning package to warehouse.")
        raise  # re-raise เพื่อให้ Task จบสถานะเป็น cancelled อย่างสมบูรณ์


async def main():
    # 1. สร้าง task สำหรับส่งพัสดุ โดยใช้เวลา 5 วินาที
    task = asyncio.create_task(
        delivery_task("P001", 5.0),
        name="Express-Courier"
    )

    # 2. ตรวจสอบสถานะของ task ทันทีหลังสร้าง
    await asyncio.sleep(2)
    print(f"[{ctime()}] Checking task '{task.get_name()}'. Is it done? {task.done()}")

    # 3. ถ้า task ยังไม่เสร็จ ให้ยกเลิก task
    if not task.done():
        print(f"[{ctime()}] Taking too long! Canceling the task...")
        task.cancel()

    # 4. รอให้ task จบสถานะ (ไม่ว่าจะสำเร็จหรือถูกยกเลิก) และจัดการ CancelledError
    try:
        await task
    except asyncio.CancelledError:
        pass

    # 5. ตรวจสอบสถานะของ task อีกครั้งหลังจากรอให้จบ
    print(f"[{ctime()}] Final verify: Is task officially canceled? {task.cancelled()}")




if __name__ == "__main__":
    asyncio.run(main())