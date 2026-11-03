import asyncio as ai


async def set_future_result(future, value):
    await ai.sleep(value)
    future.set_result(value)
    print(f"set the futures result to: {value}")
    

async def main():
    loop = ai.get_running_loop()
    future = loop.create_future()
    
    ai.create_task(set_future_result(future, "Future  result is ready"))
    
    result = await future
    print(f"Received the futur's result : {result}")
    
ai.run(main())