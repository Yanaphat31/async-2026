# นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED เท่านั้น (หากใครใช้ gather หรือ wait_for จะไม่ตรงสเปกเงื่อนไขการแข่งส่งข้อมูล)
# stock_price.py
# Assignment 2: The Stock Price Race (Mock Version)
# ต้องใช้ asyncio.wait() + return_when=asyncio.FIRST_COMPLETED เท่านั้น

import asyncio
from time import ctime

# จำลองการดึงราคาหุ้นจากเซิร์ฟเวอร์แต่ละสาขา โดยแต่ละสาขาจะมีความหน่วง (Latency) ไม่เท่ากัน
async def fetch_stock_price(server_name, delay):
    await asyncio.sleep(delay) 
    return f"[{server_name}] Price: 150 USD"


async def main():
    # 1: สร้าง Task สำหรับดึงราคาหุ้นจากเซิร์ฟเวอร์แต่ละสาขา
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0)),  # ช้าสุด
        asyncio.create_task(fetch_stock_price("Beta", 0.8)),   # เร็วสุด
        asyncio.create_task(fetch_stock_price("Gamma", 1.5)),  # ปานกลาง
    }

    # 2: แสดงข้อความว่าเริ่มการแข่งขันดึงราคาหุ้น
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3: แสดงผลลัพธ์ของ Task ที่เสร็จสมบูรณ์ก่อน
    for winner in done:
        print(f"{ctime()} Winner Result: {winner.result()}")

    # 4: ยกเลิก Task ที่ยังไม่เสร็จสมบูรณ์
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())