from time import ctime, time
import asyncio
import os
import threading

# ฟังก์ชันจำลองการทำกาแฟแบบ Asynchronous
async def make_coffee(customer_name):
    # 1. ดึง PID ของ Process (จะเหมือนกันในทุก Coroutine)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id

    # 2. ดึง Task ปัจจุบัน asyncio
    current_task = asyncio.current_task()
    task_name = current_task.get_name() if current_task else "N/A Task"

    # 3. ใน Python 3.12+ สามารถดึง unique ID ของแต่ละ Task ได้ใน asyncio
    task_id = id(current_task)

    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Async Task ID: {task_id}] [Task Name: {task_name}] กำลังชงกาแฟให้ ลูกค้า {customer_name}...")
    await asyncio.sleep(5)
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Async Task ID: {task_id}] [Task Name: {task_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

async def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] === เริ่มระบบจำลองตู้กาแฟแบบ asyncio ===")
    start_time = time()

    tasks = []
    for customer in queue:
        # สร้าง Coroutine และ Loop ผ่าน asyncio
        coro = make_coffee(customer)
        # สร้าง Task จาก Coroutine พร้อมตั้งชื่อ Task-{customer}
        task = asyncio.create_task(coro, name=f"Task-{customer}")
        tasks.append(task)

    # รอให้ทุก Task เสร็จ
    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} | ใช้เวลารวมทั้งหมด: {duration:.2f} วินาที")

if __name__ == "__main__":
    asyncio.run(main())