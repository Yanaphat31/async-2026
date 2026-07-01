# Program 2: The Coroutine Object
# Concept: Seeing that calling an async def function creates an "Object" but does not execute it yet.
import asyncio

async def greet():
    print("Hello!")

#calling the async function does not execute it, but returns a coroutine object
coroutine_object = greet()
print(type(coroutine_object))  # <class 'coroutine'>

coro_object = greet()

print(f"Coroutine object: {coro_object}")

coro_object.close(



)