import logging
import string
import asyncio
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s,%(msecs)d %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

class PubSubMessage:
    """Class for representing a message in the PubSub.
    """

    def __init__(self, instance_name, message):
        self.instance_name = instance_name
        self.message = message
        self.hostname = f'{instance_name}.example.net'

    def __str__(self):
        return f"{self.message} from {self.hostname}"

async def publish(queue, n):
    """Generates `n` random messages and pushes them 
       into the `queue`

    Args:
        queue (object): asyncio queue
        n (int): count of random messages to push
    """
    choices = string.ascii_lowercase + string.digits

    for x in range(1, n + 1):
        host_id = ''.join(random.choices(choices, k=4))
        instance_name = f'cattle-{host_id}'
        msg = PubSubMessage(instance_name, x)
        await queue.put(msg)
        logging.info(f'Published {x} of {n} messages')

    await queue.put(None)  # publisher is done


async def consume(queue):
    """_summary_

    Args:
        queue (_type_): _description_
    """
    while True:
        # wait for an item from the publisher
        msg = await queue.get()
        if msg is None:  # publisher is done
            break

        # process the msg
        logging.info(f'Consumed {msg}')
        # unhelpful simulation of i/o work
        await asyncio.sleep(random.random())


def main():
    """Main function
    """
    queue = asyncio.Queue()
    asyncio.run(publish(queue, 5))
    asyncio.run(consume(queue))


if __name__ == '__main__':
    main()