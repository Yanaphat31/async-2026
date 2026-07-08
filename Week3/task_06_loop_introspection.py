# Objective: Introspect runtime contexts and monitor open workload queues on the active loop.
import asyncio
from time import ctime

async def dynamic_job(number):
    await asyncio.sleep(1.0)

async def main():
    # ตรวจสอบ identity ของ Task ที่กำลังทำงานอยู่ในปัจจุบัน
    me = asyncio.current_task()
    me.set_name("Main-Coordinator")
    print(f"{ctime()} Active Execution Context Name: {me.get_name()}")
    
    # สร้าง background Tasks หลายรายการแบบ dynamically
    tasks = [asyncio.create_task(dynamic_job(i), name=f"Job-{i}") for i in range(3)]
    
    # ตรวจสอบ Tasks ทั้งหมดที่ยัง active อยู่ภายใน Event Loop
    all_active = asyncio.all_tasks()
    print(f"{ctime()} Total Active Tasks inside Loop: {len(all_active)}")
    for t in all_active:
        print(f"{ctime()}  -> Active Queue Item: {t.get_name()}")

    await asyncio.sleep(1.1) # รอให้ background Tasks ทั้งหมดทำงานเสร็จสิ้น

asyncio.run(main())