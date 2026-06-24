from time import sleep, ctime, time, process_time
import multiprocessing
import threading
import os
import psutil

# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คน
def make_coffee(customer_name, result_queue):
    # ดึง PID ของแต่ละ Process (จะแตกต่างกันในแต่ละตัว)
    pid = os.getpid()
    thread_id = threading.current_thread().native_id
    thread_name = threading.current_thread().name

    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] กำลังชงกาแฟให้ ลูกค้า {customer_name}...")
    start_cpu = process_time()
    sum(i * i for i in range(1000000)) # จำลองงานที่ต้องการค่าคำนวณ (CPU-bound) เล็กน้อย และรอ 5 วินาที
    sleep(5) # บล็อคการทำงานของ Thread ไว้ 5 วินาทีเต็ม
    cpu_duration = process_time() - start_cpu
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

    # ส่งค่าการใช้ RAM และ CPU ของตัวเองกลับมาให้หน้าหลักผ่าน Queue
    process = psutil.Process(pid)
    mem_mb = process.memory_info().rss / (1024 * 1024)
    result_queue.put((mem_mb, cpu_duration))

def main():
    queue = ['A', 'B', 'C']
    main_pid = os.getpid()
    main_tid = threading.current_thread().native_id

    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] === เริ่มระบบจำลองตู้กาแฟแบบ Multi-processing ===")
    start_time = time()
    main_start_cpu = process_time()

    result_queue = multiprocessing.Queue()
    processes = []
    for customer in queue:
        p = multiprocessing.Process(target=make_coffee, args=(customer, result_queue))
        processes.append(p)
        p.start()

    child_memories = []
    child_cpu_times = []
    for _ in queue:
        mem, cpu_t = result_queue.get()
        child_memories.append(mem)
        child_cpu_times.append(cpu_t)

    for p in processes:
        p.join()

    duration = time() - start_time

    main_process = psutil.Process(os.getpid())
    main_mem = main_process.memory_info().rss / (1024 * 1024)

    total_memory = main_mem + sum(child_memories)
    total_cpu = (process_time() - main_start_cpu) + sum(child_cpu_times)

    print(f"[โหมด Multi-processing]")
    print(f"เวลาที่ใช้จริง (Wall Time): {duration:.2f} วินาที")
    print(f"เวลาที่ใช้บน CPU ทุก Core ที่แต่ละ Process ใช้ (Total CPU Time): {total_cpu:.4f} วินาที")
    print(f"หน่วยความจำ (RAM) รวมทุก Process: {total_memory:.2f} MB [Main: {main_mem:.2f} MB + รวม: {sum(child_memories):.2f} MB]")

if __name__ == "__main__":
    main()