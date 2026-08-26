import asyncio
import random

# ================= Stage 1: Scraper (Producer) =================
async def scraper(queue: asyncio.Queue):
    # จำลองการ scrape 5 หน้าเว็บ เพื่อเก็บ URL ของไฟล์ที่ต้องดาวน์โหลด
    for page in range(1, 6):
        await asyncio.sleep(random.uniform(0.3, 0.8))  # จำลองเวลา scrape แต่ละหน้า

        url = f"https://example.com/files/file-{page}.zip"
        print(f"[Scraper]     เจอลิงก์จากหน้า {page}: {url}")

        # ส่งงานต่อให้ฝั่ง Downloader ผ่านคิว
        # (ถ้าคิวเต็ม maxsize จะหยุดรอที่นี่ = Backpressure)
        await queue.put(url)

    print("[Scraper]     scrape ครบทุกหน้าแล้ว!")

# ================= Stage 2: Downloader (Consumer) =================
async def downloader(downloader_id: int, queue: asyncio.Queue):
    while True:
        # ดึง URL ออกจากคิว (ถ้าคิวว่างจะรอที่นี่)
        url = await queue.get()

        print(f"[Loader-{downloader_id}] เริ่มดาวน์โหลด: {url}")
        await asyncio.sleep(random.uniform(1.0, 2.0))  # จำลองเวลาดาวน์โหลด

        print(f"[Loader-{downloader_id}] ดาวน์โหลด {url} เสร็จ!")
        # แจ้ง Queue ว่างานชิ้นนี้เสร็จสมบูรณ์แล้ว
        queue.task_done()

async def main():
    # จำกัดความจุของคิวไว้ที่ 2
    queue = asyncio.Queue(maxsize=2)

    # 1. Stage 1: สร้าง Scraper ผลิต URL ใส่คิว
    producer = asyncio.create_task(scraper(queue))

    # 2. Stage 2: สร้าง Downloader 2 ตัว รันขนานกันเป็น background tasks
    consumers = []
    for i in range(1, 3):
        task = asyncio.create_task(downloader(i, queue))
        consumers.append(task)

    # 3. รอให้ Scraper scrape จนครบทุกหน้า
    await producer

    # 4. รอให้ทุก URL ในคิวถูกดาวน์โหลดเสร็จ (task_done ครบทุกชิ้น)
    await queue.join()

    print("=== ดาวน์โหลดครบทุกไฟล์เรียบร้อยแล้ว! ===")

    # 5. ยกเลิก Downloader ที่ยังรองานบนคิวอยู่ใน Background
    for task in consumers:
        task.cancel()

if __name__ == "__main__":
    asyncio.run(main())

