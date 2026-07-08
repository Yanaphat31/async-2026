# Objective: Implement complex processing workflows based on task fulfillment conditions.
import asyncio
from time import ctime

async def network_probe(server_name, delay):
    await asyncio.sleep(delay)
    return f"Ping successful: {server_name}"

async def main():
    # asyncio.wait() จะรอจนกว่า Task อย่างน้อยหนึ่งตัวทำงานเสร็จสิ้น เสร็จ 1 / เอาออกมาเยกเลิก Task ที่เหลือ
    tasks = {
        asyncio.create_task(network_probe("Primary-Server", 2.0)),
        asyncio.create_task(network_probe("Backup-Server-1", 0.5)),
        asyncio.create_task(network_probe("Backup-Server-2", 1.0))
    }
    
    #  รอจนกว่า Task อย่างน้อยหนึ่งตัวทำงานเสร็จสิ้น
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    
    print(f"{ctime()} Count of Tasks Done: {len(done)}")       # แสดงจำนวน Task ที่ทำงานเสร็จสิ้น
    print(f"{ctime()} Count of Tasks Pending: {len(pending)}") # แสดงจำนวน Task ที่ยังไม่เสร็จ
    
    for finished_task in done:
        print(f"{ctime()} Fastest Task Result: {finished_task.result()}")
        
    # ยกเลิก Task ที่ยังไม่เสร็จ
    for ongoing_task in pending:
        ongoing_task.cancel()

asyncio.run(main())