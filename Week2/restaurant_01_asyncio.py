from time import ctime, time
import asyncio



async def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    await asyncio.sleep(1)  # non-blocking delay (was: sleep(1))
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


async def customer_private_workflow(customer):
    print(f"{ctime()}   [Task-{customer}] Taking Order ...")
    await asyncio.sleep(1)  # Simulate a delay in taking order
    print(f"{ctime()}   [Task-{customer}] Taking Order ...Done!")


    print(f"{ctime()}   [Task-{customer}] Cooking Spaghetti ...")
    await asyncio.sleep(1)  # Simulate a delay in cooking
    print(f"{ctime()}   [Task-{customer}] Cooking Spaghetti ...Done!")


    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...")
    await asyncio.sleep(1)  # Simulate a delay in preparing the drink
    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...Done!")
    print(f"{ctime()}   [Task-{customer}] All served!\n")


async def main():
    customers = ["A", "B", "C"]
    start_time = time()

    for customer in customers:
        await greet_diners(customer)

    print(f"\n{ctime()} --- All customers greeted. Scheduling independent Async Tasks! ---\n")

    
    tasks = [asyncio.create_task(customer_private_workflow(c)) for c in customers]

  
    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())