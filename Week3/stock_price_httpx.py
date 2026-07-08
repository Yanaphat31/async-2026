# stock_price_httpx.py (เวอร์ชันสำหรับแจกเป็นโจทย์หรือแนวทางให้นักเรียนเขียน)
# stock_price_httpx.py
# Assignment 3: Concurrency Racing on Live Network (FastAPI + HTTPX)

import asyncio
import httpx
from time import ctime

# ทดสอบบนเครื่องตัวเอง: 127.0.0.1 | เซิร์ฟเวอร์อาจารย์ในห้อง: 172.16.2.117
BASE_URL = "http://127.0.0.1:8088"


async def fetch_stock_price(server_name: str):
    """เชื่อมต่อ Mock Server (ห้ามรับ delay - ความหน่วงเกิดจริงที่ฝั่ง API)"""
    url = f"{BASE_URL}/price/{server_name}"

    # ใช้ httpx.AsyncClient ผ่าน async with เพื่อไม่ Block Event Loop
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"


async def main():
    # แปลงคูรูทีนทั้ง 3 สาขาเป็น Task ส่งเข้าคิวรันพร้อมกันใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha")),   # หน่วง 3.0s ที่ฝั่ง server
        asyncio.create_task(fetch_stock_price("Beta")),    # หน่วง 0.8s (คาดหวังผู้ชนะ)
        asyncio.create_task(fetch_stock_price("Gamma")),   # หน่วง 1.5s
    }

    # asyncio.wait + FIRST_COMPLETED -> ดีดหลุดทันทีที่เซิร์ฟเวอร์ตัวแรกตอบกลับ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # แสดงผลลัพธ์ผู้ชนะการแข่งขัน
    for winner in done:
        print(f"{ctime()} Winner Result: {winner.result()}")

    # [Anti-Memory Leak] วนลูปยกเลิกงาน pending ตัดสัญญาณ Network ที่ค้างอยู่
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())