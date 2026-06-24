from time import ctime, time, process_time
import asyncio
import os
import threading
import psutil

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    # 1. ดึง PID ของ Process และ Thread ID (จะเหมือนกันในทุก Coroutine)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id

    # 2. ดึงงาน Task ปัจจุบัน asyncio
    current_task = asyncio.current_task()
    task_name = current_task.get_name() if current_task else "N/A Task"

    # 3. ใน Python 3.12+ สามารถดึง Unique ID ของแต่ละ Task ได้ใน asyncio
    task_id = id(current_task)

    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Async Task ID: {task_id}] [Task Name: {task_name}] กำลังชงกาแฟให้ ลูกค้า {customer_name}...")
    sum(i + 1 for i in range(1000000)) # จำลองงานที่ต้องการค่าคำนวณ (CPU-bound) เล็กน้อย และรอ 5 วินาที
    await asyncio.sleep(5) # Non-blocking wait
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Async Task ID: {task_id}] [Task Name: {task_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

async def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] === เริ่มระบบจำลองตู้กาแฟแบบ asyncio ===")
    start_time = time()
    start_cpu = process_time()

    tasks = []
    for customer in queue:
        # สร้าง Coroutine และใส่ใน Event Loop ผ่าน asyncio แล้วตั้งชื่อได้
        coro = make_coffee(customer)
        # ส่ง Coroutine ไปยัง Task จากนั้น asyncio จะจัดการให้
        task = asyncio.create_task(coro, name=f"Task-{customer}")
        tasks.append(task)

    # รอให้ทุก Task เสร็จ
    await asyncio.gather(*tasks)

    duration = time() - start_time
    cpu_duration = process_time() - start_cpu

    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)

    print(f"[โหมด Asyncio]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลาที่ใช้บน CPU (CPU Time): {cpu_duration:.4f} วินาที")
    print(f"หน่วยความจำ (RAM) ที่ใช้: {mem_mb:.2f} MB")

if __name__ == "__main__":
    asyncio.run(main())