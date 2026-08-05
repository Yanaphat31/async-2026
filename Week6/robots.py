import asyncio
import time
import http
from xmlrpc import client
import httpx

import asyncio                                      # ใช้รันโปรแกรมแบบ Asynchronous
import aiohttp                                      # ใช้ส่ง HTTP Request แบบ Async
import time                     








# ==========================================
# 1. Configuration & Constants
# ==========================================
STUDENT_ID = "6720301001" 
BASE_URL = "http://172.16.2.117:8088"

# กำหนดลำดับชิ้นส่วนและหุ่นยนต์
PARTS = ["A", "B", "C"]
ROBOTS = ["robot_1", "robot_2", "robot_3"]

# ==========================================
# 2. Async Functions Development
# ==========================================

async def reset_factory(client: httpx.AsyncClient):
    """ส่ง Request เพื่อทำการ Reset สถานะของหุ่นยนต์ทั้งหมดของรหัสนักเรียนนี้"""
    url = f"{BASE_URL}/api/{STUDENT_ID}/reset"
    response = await client.post(url)
    if response.status_code == 200:
        print("Factory reset successful.")


async def grab_part(client: httpx.AsyncClient, robot_id: str, part: str):
    """สั่งให้หุ่นยนต์หยิบชิ้นส่วน 1 ชิ้น"""
    url = f"{BASE_URL}/api/{STUDENT_ID}/robots/{robot_id}/grab"
    payload = {"part": part}
    response = await client.post(url, json=payload)
    if response.status_code == 200:
        print(f"{robot_id} grabbed part {part}.")
    else:
        print(f"Failed to grab part {part} with {robot_id}. Status code: {response.status_code}")






async def run_robot_task(client: httpx.AsyncClient, robot_id: str):
    """สั่งให้หุ่นยนต์ 1 ตัว ทำการหยิบชิ้นส่วน A, B, และ C ตามลำดับ"""
    for part in PARTS:
        await grab_part(client, robot_id, part)
        await asyncio.sleep(1)  


    

async def main():
    """ฟังก์ชันหลักสำหรับเริ่มการทำงานของหุ่นยนต์ทั้ง 4 ตัวแบบ Async"""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("Resetting Factory...")
        await reset_factory(client)
        
        start_time = time.time()
        print("Starting Async Robot Operation...")
        
       
        tasks = [run_robot_task(client, robot_id) for robot_id in ROBOTS]
        await asyncio.gather(*tasks) 
        
        elapsed_time = time.time() - start_time
        print(f"Finished all tasks in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())


