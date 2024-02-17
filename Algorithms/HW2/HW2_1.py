from queue import Queue
import time
from datetime import datetime
from random import randint

queue = Queue()

def generate_request():
    client = datetime.now().strftime("%H%M%S")
    queue.put(client)
    print(f'Відвідувач {client} доданий в чергу.')

def process_request():
    if not queue.empty():
        client = queue.get()
        print(f'Відвідувача {client} обслуговано.')
    else:
        print('Черга пуста.')


counter = 0
while counter < 30:
    rand = randint(1,11)
    if rand % 2 == 0:
        generate_request()
    else:
        process_request()
    counter += 1
    time.sleep(1)

