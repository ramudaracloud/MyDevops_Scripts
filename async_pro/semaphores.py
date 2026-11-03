import asyncio as ai


async def access_resources(semaphore, resource_id):
    async with semaphore:
        print(f"Accessing resource {resource_id}")
        await ai.sleep(1)
        print(f"Releasing resource: {resource_id}")
        
async def main():
    semaphore = ai.Semaphore(2)
    await ai.gather(*(access_resources(semaphore, i) for i in range(5)))

ai.run(main())
    
    