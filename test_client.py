"""
test_client.py
"""
from datetime import datetime
import logging
import requests
import threading

logging.basicConfig(level=logging.DEBUG)

SESSION = requests.Session()
CONCURRENT_REQUESTS = 20
RESULTS = []


def run(url):
    response = SESSION.get(url)


def test_tornado_async():
    """
    """
    time = run_threads('http://localhost:8888/async')
    RESULTS.append(('Tornado async', time))


def test_tornado_sync():
    """
    """
    time = run_threads('http://localhost:8888/sync')
    RESULTS.append(('Tornado sync', time))


def test_flask_sync():
    time = run_threads('http://localhost:5001/sync')
    RESULTS.append(('Flask sync', time))


def run_threads(*args):
    """
    """
    start = datetime.utcnow()

    workers = [
        threading.Thread(target=run, args=args) for _ in range(CONCURRENT_REQUESTS)]

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    return datetime.utcnow() - start


if __name__ == '__main__':
    test_tornado_async()
    # test_tornado_sync()
    test_flask_sync()

    for res in RESULTS:
        print('{:<14} {}'.format(*res))

