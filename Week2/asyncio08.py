# Program 8: Task Interleaving (Context Switching)
# Concept: Watching a single thread switch back and forth between two different workflows using create_task.

import asyncio
from asyncio import sleep
from time import time, ctime

async def kitchen_crew():
    print(f"{ctime()} -> [Chef] puts noodle in boiling water...")
    await sleep(1)  # Simulate time taken to prepare ingredients
    print(f"{ctime()} -> [Chef] Ingredients are ready!")


async def bar_crew():
    print(f"{ctime()} -> [Bar] starta grinding coffee beans...")
    await sleep(1)  # Simulate time taken to prepare drinks
    print(f"{ctime()} -> [Bar] Drinks are ready!")

async def main():
    task_kitchen = asyncio.create_task(kitchen_crew())
    task_bar = asyncio.create_task(bar_crew())

    await task_kitchen
    await task_bar

if __name__ == "__main__":
    asyncio.run(main())