import asyncio
import aiohttp
import time

BASE = "http://172.16.2.117:8088"
STUDENT_ID = "6720301001"
LIGHT_IDS = ["light_1", "light_2", "light_3", "light_4"]


async def turn_on(session: aiohttp.ClientSession, light_id: str):
    url = f"{BASE}/api/{STUDENT_ID}/lights/{light_id}"
    async with session.post(url, json={"status": "ON"}) as resp:
        data = await resp.json()
        print(f" {light_id} -> {resp.status}")
        return data


async def main():
    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [turn_on(session, lid) for lid in LIGHT_IDS]
        results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"\n  เปิดไฟทั้งหมดเสร็จใน {elapsed:.2f} วินาที")


if __name__ == "__main__":
    asyncio.run(main())