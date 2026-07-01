# Program 9: Dynamically Tracking Tasks in a List
# Concept: Managing multiple generated tasks dynamically by appending them into a standard Python list.
import asyncio
from asyncio import sleep
from time import time, ctime

async def sever_customer(name):
    print(f"{ctime()} -> Serving customer: {name}...")
    await sleep(1)  # Simulate time taken to serve customer
    print(f"{ctime()} -> Served {name}")

async def main():
    start = time()
    customer = ["A", "B", "C", "D"] 
    tasks = []  # List to hold the tasks


    for name in customer:
        task = asyncio.create_task(sever_customer(name))  # Create a task for each customer
        tasks.append(task)  # Append the task to the list


    for task in tasks:
        await task  # Await each task to ensure they complete

    print(f"Total time: {time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine
    