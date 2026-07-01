# Program: Creating Concurrent Tasks with Threading
# Concept: Greeting customers one by one, then handling each customer's workflow concurrently.

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

    # Step 1: Greet customers one by one
    for customer in customers:
        greet_diners(customer)

    print(f"{ctime()} -> Finished greeting in {time() - start_time:.2f} seconds")

    # Step 2: Create threads for each customer's private workflow
    threads = []

    for customer in customers:
        task = threading.Thread(target=customer_private_workflow, args=(customer,))
        threads.append(task)
        task.start()

    # Step 3: Wait for all threads to finish
    for task in threads:
        task.join()

    print(f"{ctime()} -> Finished all tasks in {time() - start_time:.2f} seconds")