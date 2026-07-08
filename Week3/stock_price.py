# นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED เท่านั้น (หากใครใช้ gather หรือ wait_for จะไม่ตรงสเปกเงื่อนไขการแข่งส่งข้อมูล)
# stock_price.py
# Assignment 2: The Stock Price Race (Mock Version)
# ต้องใช้ asyncio.wait() + return_when=asyncio.FIRST_COMPLETED เท่านั้น

import asyncio
from time import ctime


# ข้อ 1: Coroutine จำลองดึงราคาหุ้น ด้วย asyncio.sleep(delay)
async def fetch_stock_price(server_name, delay):
    await asyncio.sleep(delay)  # จำลองความหน่วงอินเทอร์เน็ตของแต่ละสาขา
    return f"[{server_name}] Price: 150 USD"


async def main():
    # 2: แตก Task 3 ตัวพร้อมกันใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0)),  # ช้าสุด
        asyncio.create_task(fetch_stock_price("Beta", 0.8)),   # เร็วสุด
        asyncio.create_task(fetch_stock_price("Gamma", 1.5)),  # ปานกลาง
    }

    # 3: asyncio.wait + FIRST_COMPLETED -> ดีดหลุดจากการรอทันทีที่ตัวแรกเสร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 4: แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน
    for winner in done:
        print(f"{ctime()} Winner Result: {winner.result()}")

    # 5: วนลูปเคลียร์ระบบ ยกเลิกงาน pending ที่เหลือ ป้องกัน Memory Leak
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())