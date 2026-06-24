from time import sleep, ctime, time, process_time
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name):
    # ดึง PID ของระบบ (จะเหมือนกันทุก Thread)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] กำลังชงกาแฟให้ ลูกค้า {customer_name}...")
    sum(i + 1 for i in range(1000000)) # จำลองงานที่ต้องการ CPU (CPU-bound) เพิ่มขึ้น 5 วินาที
    sleep(5) # บล็อคการทำงานของ Thread ไว้ 5 วินาทีเต็ม
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] === เริ่มระบบจำลองตู้กาแฟแบบ Multi-Thread ===")
    start_time = time()
    start_cpu = process_time() # เริ่มนับเวลา CPU

    threads = []
    # ลูปสร้างงาน Thread
    for customer in queue:
        # เราสามารถตั้งชื่อ Thread ผ่านพารามิเตอร์ name= ได้เพื่อให้ได้ค้นหาได้ง่ายขึ้น
        t = threading.Thread(target=make_coffee, args=(customer,), name=f"Thread-{customer}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time() - start_time
    cpu_duration = process_time() - start_cpu

    # ใช้ psutil ดึงการใช้งาน RAM
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)

    print(f"[โหมด Multi-Thread]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลาที่ใช้บน CPU (CPU Time): {cpu_duration:.4f} วินาที")
    print(f"หน่วยความจำ (RAM) ที่ใช้: {mem_mb:.2f} MB")

if __name__ == "__main__":
    main()