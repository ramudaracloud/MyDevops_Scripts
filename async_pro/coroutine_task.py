import asyncio as ai


async def fetch_data(delay, id):
    print("Fetching data....id",id)
    await ai.sleep(delay)
    print("Data Fetched, id:", id)
    return {"data":"Some Data", "id:":id}

async def main():
    task1 = fetch_data(10, 1)
    task2 = fetch_data(30, 2)
    task3 = fetch_data(2, 3)
    
    result1 = await task1
    result2 = await task2
    result3 = await task3
    print(f"received resullt : {result1}" )
    print(f"received resullt : {result2}" )
    print(f"received resullt : {result3}" )
    
# Run the main coroutine
ai.run(main())
    
    
    