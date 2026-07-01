# Program 10: Extracting Return Values from Tasks
# Concept: Accessing returned results from completed Task objects using .result() or direct assignment.
import asyncio

async def calculate_bille(customer, base_price):
    print(f"Calculating bill for {customer}...")

    await asyncio.sleep(1)  # Simulate time taken to calculate bill
    total = base_price * 1.07  # Adding tax
    return total

async def main():
    # Create a task for calculating the bill
    task_bill_a = asyncio.create_task(calculate_bille("A", 100))
    task_bill_b = asyncio.create_task(calculate_bille("B", 200))

    result_a = await task_bill_a  # Await the task to get the result
    result_b = await task_bill_b  # Await the second task to get the result


    print(f"Total bill for customer A: ${result_a:.2f}")
    print(f"Total bill for customer B: ${result_b:.2f}")

if __name__ == "__main__":
    asyncio.run(main())  # This will execute the main coroutine



   