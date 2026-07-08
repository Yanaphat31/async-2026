# Objective: Attach a plain synchronous function that automatically triggers the moment a task finishes.
import asyncio
from time import ctime

def alert_manager(finished_task):
    # callback function ที่จะถูกเรียกเมื่อ Task ทำงานเสร็จสิ้น
    print(f"{ctime()} Callback Triggered! Task output fetched: {finished_task.result()}")

async def download_file():
    print(f"{ctime()} Downloading packet...")
    await asyncio.sleep(1.0)
    return "Data_Payload.zip"

async def main():
    task = asyncio.create_task(download_file())

    # register callback function ที่จะถูกเรียกอัตโนมัติเมื่อ Task ทำงานเสร็จสิ้น
    task.add_done_callback(alert_manager)
    
    await task  # รอให้ Task ทำงานเสร็จและ trigger callback function

asyncio.run(main())