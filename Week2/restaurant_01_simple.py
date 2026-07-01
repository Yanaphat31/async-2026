# Program: Creating Concurrent Tasks with Threading
# Concept: Greeting customers one by one, then handling each customer's workflow concurrently.
import asyncio
import threading
from time import time, ctime, sleep


def greet_diners(customer):
    print(f"{ctime()} -> Greeting customer {customer}...")
    sleep(1)
    print(f"{ctime()} -> Greeting customer {customer} done!")


def customer_private_workflow(customer):
    print(f"{ctime()} -> Taking order for customer {customer}...")
    sleep(1)
    print(f"{ctime()} -> Taking order for customer {customer} done!")

    print(f"{ctime()} -> Cooking for customer {customer}...")
    sleep(1)
    print(f"{ctime()} -> Cooking for customer {customer} done!")

    print(f"{ctime()} -> Serving mini bar for customer {customer}...")
    sleep(1)
    print(f"{ctime()} -> Serving mini bar for customer {customer} done!")


if __name__ == "__main__":
    start_time = time()

    customers = ["A", "B", "C"]

for customer in customers:
    greet_diners(customer)

print(f"{ctime()} -> Finished greeting in {time() - start_time:.2f} seconds")


processes = []
for customer in customers:
    task = threading.Thread(target=customer_private_workflow, args=(customer,))
    processes.append(task)
    task.start()

for task in processes:
    task.join()

duration = time() - start_time
print(f"{ctime()} -> Finished all tasks in {duration:.2f} seconds")

