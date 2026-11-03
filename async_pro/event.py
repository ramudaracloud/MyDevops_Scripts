import asyncio as ai


async def waiter(event):
    print("Waiting for the event to be set")
    await event.wait()
    print("event has been set , continuing execution")
    
    
async def setter(event):
    await ai.sleep(2)
    event.set()
    print("event has been set")
    
async def main():
    event = ai.Event()
    await ai.gather(waiter(event), setter(event))
    
ai.run(main())
    