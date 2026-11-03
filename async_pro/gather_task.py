import asyncio as ai


async def fetch_data(id, sleep_time):
    print(f"coroutine {id} starting to fetch data")
    await ai.sleep(sleep_time)
    return {"id":id, "data": f"sample data from coroutine {id}"}

async def main():
    results = await ai.gather(fetch_data(1,20),
                              fetch_data(2,30),
                              fetch_data(3,15))
    
    for result in results:
        print(f"Received result : {result}")
        
ai.run(main())
    