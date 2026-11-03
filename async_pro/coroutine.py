import asyncio as ai


async def fetch_data(delay):
  print("Fetching data....")
  await ai.sleep(delay)
  print("Data Fetched")
  return {"data":"Some Data"}

async def main():
  print("Start of main coroutine")
  task = fetch_data(5)
  # await the task to complete and get the result
  result = await task

  print(f"Received results: {result}")
  print("End of main Coroutine")

ai.run(main())