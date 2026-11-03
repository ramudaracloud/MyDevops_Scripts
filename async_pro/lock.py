import asyncio as ai

shared_resource = 0
lock = ai.Lock()

async def modify_shared_resource():
    global shared_resource
    
    async with lock:
        print(f"Resource before modification {shared_resource}")
        shared_resource +=1
        await ai.sleep(1)
        print(f"Resources after modification {shared_resource}")
        

async def main():
    await ai.gather(*(modify_shared_resource() for _ in range(5)))

ai.run(main())