import asyncio as ai


async def fetch_data(id, sleep_time):
    print(f"coroutine {id} starting to fetch data")
    await ai.sleep(sleep_time)
    return {"id":id, "data": f"sample data from coroutine {id}"}


async def main():
    # create tasks for running coroutines concurrently
    task1 = ai.create_task(fetch_data(1, 20))
    task2 = ai.create_task(fetch_data(2, 3))
    task3 = ai.create_task(fetch_data(3, 5))
    
    result1 = await task1
    result2 = await task2
    result3 = await task3
    
    print(f"Received result: {result1, result2, result3}")
    
    
ai.run(main())