import asyncio
import httpx


SERVER_URL = "http://172.20.56.245:8000"

MY_STUDENT_ID = "6720301001"


async def hunt_coupons():

    async with httpx.AsyncClient() as client:


        print(f"[{MY_STUDENT_ID}] เริ่มต้นการล่าคูปอง...")

        for attempt in range(1, 6):

            try:
                res = await client.post(
                    f"{SERVER_URL}/claim",
                    json={"student_id": MY_STUDENT_ID},
                    timeout=5.0
                )

                data = res.json()
                status = data.get("status")

                print(
                    f"ครั้งที่ {attempt}: [{status}] "
                    f"-> {data.get('message', data.get('claimed_coupon'))}"
                )

                if status in ["LIMIT_REACHED", "OUT_OF_STOCK"]:
                    break

            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

            await asyncio.sleep(0.02)


        print("\nกำลังดึงสรุปคูปองของตนเอง...")

        try:
            res = await client.get(
                f"{SERVER_URL}/my-coupons/{MY_STUDENT_ID}"
            )

            if res.status_code == 200:

                summary = res.json()

                total = summary.get("total_claimed", 0)
                coupons = summary.get("claimed_coupons", [])

                print(
                    f"สรุปผล [{MY_STUDENT_ID}]: "
                    f"ได้รับคูปองรวม {total} ใบ -> {coupons}"
                )

            else:
                print(
                    f"ดึงข้อมูลส่วนตัวไม่สำเร็จ Status Code: {res.status_code}"
                )

        except Exception as e:
            print(
                f"เกิดข้อผิดพลาดในการดึงข้อมูลส่วนตัว: {e}"
            )


        print("\nกำลังดึงสรุปภาพรวมทั้งหมดจาก Server (/summary)...")

        try:
            res = await client.get(
                f"{SERVER_URL}/summary"
            )

            if res.status_code == 200:

                summary_all = res.json()

                rem_stock = summary_all.get(
                    "remaining_stock",
                    "N/A"
                )

                claims = summary_all.get(
                    "student_claims",
                    {}
                )

                print(
                    f"จำนวนคูปองเหลือใน Server: {rem_stock} ใบ"
                )

                print("รายการคูปองที่นักเรียนแต่ละคนได้รับ:")

                for sid, coupons in claims.items():

                    print(
                        f"{sid}: ได้ {len(coupons)} ใบ -> {coupons}"
                    )

            else:

                print(
                    f"ดึงข้อมูลสรุปภาพรวมไม่สำเร็จ Status Code: {res.status_code}"
                )

        except Exception as e:

            print(
                f"เกิดข้อผิดพลาดในการดึงสรุปภาพรวม: {e}"
            )


if __name__ == "__main__":
    asyncio.run(hunt_coupons())