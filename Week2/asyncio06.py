# Program 6: Creating a Concurrent Task
# Concept: Wrapping a coroutine inside asyncio.create_task()
# to schedule it to run in the background.

import asyncio
from asyncio import sleep
from time import time, ctime


async def cook_spaghetti(customer):
    print(f"{ctime()} -> Cooking spaghetti for {customer}...")
    await sleep(2)  # Simulate time taken to cook spaghetti
    print(f"{ctime()} -> Spaghetti ready for {customer}!")


async def main():
    start = time()

    # Create a task for cooking spaghetti
    task_A = asyncio.create_task(cook_spaghetti("A"))

    # Do other things while the spaghetti is cooking
    print(f"{ctime()} -> Main program can do other things while task A runs in background...")

    # Wait for the spaghetti to be ready
    await task_A

    print(f"Total time: {time() - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())