# Objective: Stop an ongoing execution prematurely by triggering a cancellation exception.
import asyncio
from time import ctime

async def background_loop():
    try:
        print(f"{ctime()} Worker: Starting long infinite process...")
        while True:
            await asyncio.sleep(1)
            print(f"{ctime()} Worker: Still ticking...")
    except asyncio.CancelledError:
        # เกิดขึ้นเมื่อ task.cancel() ถูกเรียก และ Task ไปถึง checkpoint ถัดไป
        print(f"{ctime()} Worker: Interrupted! Executing clean-up logic before exit...")

async def main():
    task = asyncio.create_task(background_loop())
    await asyncio.sleep(2.5) # ปล่อยให้ background task ทำงานสักระยะ
    
    print(f"{ctime()} Main: Changing plans, canceling the worker task now!")
    task.cancel() # ส่งคำขอยกเลิก Task ที่กำลังทำงาน
    await asyncio.sleep(0.1) # เปิดโอกาสให้ Task ประมวลผลการยกเลิก

asyncio.run(main())