import asyncio, websockets, json

async def main():
    host = "xxx.xxx.x.xx"   # change to your device IP
    port = 3000

    uri = f"ws://{host}:{port}/live"
    async with websockets.connect(uri) as ws:
        print("Connected → sending login")
        await ws.send(json.dumps({"type": "login", "value": ""}))

        async for msg in ws:
            print("Received:", msg)

if __name__ == "__main__":
    asyncio.run(main())
