# Program 7: Dual Tasks Concurrency
# Concept: Scheduling two distinct tasks concurrently
# and awaiting them individually without gather.

import asyncio
from asyncio import sleep
from time import time, ctime


async def cook_spaghetti(customer):
    print(f"{ctime()} -> Cooking spaghetti for {customer}...")
    await sleep(2)  # Simulate time taken to cook spaghetti
    print(f"{ctime()} -> Spaghetti ready for {customer}!")


async def main():
    start = time()

    # Create two tasks for cooking spaghetti
    task_a = asyncio.create_task(cook_spaghetti("A"))
    task_b = asyncio.create_task(cook_spaghetti("B"))

    # Do other things while both tasks are running
    print(f"{ctime()} -> Main program can do other things while task A and task B run in background...")

    # Wait for both tasks to finish
    await task_a
    await task_b

    print(f"Total time: {time() - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())