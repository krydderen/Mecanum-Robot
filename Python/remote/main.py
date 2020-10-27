import logging
from threading import Thread

# Importing utils
from utils.client import Client


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    client = Client()
    client.start()
    sendthread = Thread(target=client.handle_send, args=(), daemon=True)
    readthread = Thread(target=client.handle_read, args=(), daemon=True)
