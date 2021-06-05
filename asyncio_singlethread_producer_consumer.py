import asyncio
from asyncio import Queue
import random

from typing import Dict


QUEUES: Dict[int, Queue[int]] = {}


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(producer())
    loop.create_task(consumer())

    loop.run_forever()


async def producer() -> None:
    QUEUES[0] = Queue()

    while True:
        await asyncio.sleep(1)

        event_data = random.randint(1, 10)
        print('event:', event_data)

        if event_data in QUEUES:
            await QUEUES[event_data].put(event_data)

        await QUEUES[0].put(event_data)


async def consumer() -> None:
    while True:
        data = await QUEUES[0].get()
        print('got data:', data)

        if data > 7:
            new_data = await wait_for(7)
            print('fetched:', new_data)


async def wait_for(data: int) -> int:
    waiting_queue: Queue[int] = Queue()

    QUEUES[data] = waiting_queue
    print('trying to fetch')
    # NOTE: For no timeout:
    # data = await waiting_queue.get()
    try:
        await asyncio.wait_for(waiting_queue.get(), timeout=5)
    except asyncio.TimeoutError:
        return -1

    return data


if __name__ == '__main__':
    main()
