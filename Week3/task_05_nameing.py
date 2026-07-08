# Objective: Label task objects explicitly to simplify logging and production tracking.
import asyncio
from time import ctime

async def background_worker():
    await asyncio.sleep(0.1)

async def main():
    task = asyncio.create_task(background_worker())
    
    # ชื่อเริ่มต้นที่ Python framework สร้างให้อัตโนมัติ
    print(f"{ctime()} Initial Name: {task.get_name()}") # ตัวอย่าง: Task-2
    
    # กำหนดชื่อ Task ใหม่เพื่อให้ง่ายต่อการ logging และ tracking
    task.set_name("Payment-Gateway-Validator")
    print(f"{ctime()} Updated Name: {task.get_name()}") # แสดงชื่อ Task ที่กำหนดใหม่

asyncio.run(main())