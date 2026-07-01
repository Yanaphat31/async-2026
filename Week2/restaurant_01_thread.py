# Program: Restaurant Operation with Async Tasks
# Concept: Greet customers one by one, then schedule independent async tasks.

import asyncio
from time import time, ctime




async def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")





async def customer_private_workflow(customer):
    task_name = f"Task-{customer}"

    print(f"{ctime()} [{task_name}] Taking Order ...")
    await asyncio.sleep(1)
    print(f"{ctime()} [{task_name}] Taking Order ...Done!")

    print(f"{ctime()} [{task_name}] Cooking Spaghetti ...")
    await asyncio.sleep(1)
    print(f"{ctime()} [{task_name}] Cooking Spaghetti ...Done!")

    print(f"{ctime()} [{task_name}] Manage Bar for Drink ...")
    await asyncio.sleep(1)
    print(f"{ctime()} [{task_name}] Manage Bar for Drink ...Done!")

    print(f"{ctime()} [{task_name}] All served!")




async def main():
    start_time = time()

    customers = ["A", "B", "C"]

  
    for customer in customers:
        await greet_diners(customer)
    print(f"\n{ctime()} --- All customers greeted. Scheduling independent Async Tasks! ---\n")




    
    task_a = asyncio.create_task(customer_private_workflow("A"))
    task_b = asyncio.create_task(customer_private_workflow("B"))
    task_c = asyncio.create_task(customer_private_workflow("C"))

    

    await task_a
    await task_b
    await task_c



    duration = time() - start_time
    print(f"\n{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())