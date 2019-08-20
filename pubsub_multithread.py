"""
Code Source: https://github.com/schollii/pypubsub/blob/master/examples/multithreadloop.py

Original Author and Licence
Oliver Schoenborn
May 2009
:copyright: Copyright 2008-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

"""

from queue import Queue
import time
import threading
import sys
from pubsub import pub

resultStep = 1000000  # the number of counts for thread resuslt to be available


def threadObserver(transfers, threadObj, count):
    """
    Listener that listens for data from testTopic. This function doesn't know where the data comes from.
    Nor the thread where the data was generated.
    :param transfers: number of transfers
    :param threadObj: threadObj is the thread in which the threadObserver is called
    :param count: current count passed in
    :return: nothing
    """
    print(transfers, threadObj, count / resultStep)


pub.subscribe(threadObserver, 'testTopic')


def onIdle():
    """
    This should be registered with gui to be called when gui is idle so we get a chance to transfer data from auxillary
    thread without blocking the gui. This function must spend as little time as possible so  gui remains responsive
    :return:
    """
    thread.transferData()


class ParallelFunction(threading.Thread):
    """
    Represent a function running in parallel thread. The thread just increments a counter and puts the counter value on
    a synchronized queue every resultStep counts. The content of the queue can be published by calling transferData()
    """

    def __init__(self):
        super().__init__()
        self.running = False  # set to True when thread should stop
        self.count = 0  # workload: keep counts
        self.queue = Queue()  #to transfer data to main thread
        self.transfer = 0  # count how many transfers occured

    def run(self):
        print('aux thread started')
        self.running = True
        while self.running:
            self.count += 1
            if self.count % resultStep == 0:
                self.queue.put(self.count)

        print('aux thread done')

    def stop(self):
        self.running = False

    def transferData(self):
        """
        Send the data from aux thread to main thread. The data was put in self.queue by the aux thread, and this queue
        is a Queue.Queue which is a synchronized queue for inter-thread communication.
        Note: This must be called from main thread.
        :return: nothing
        """
        self.transfer += 1
        while not self.queue.empty():
            pub.sendMessage('testTopic',
                            transfers=self.transfer,
                            threadObj=threading.current_thread(),
                            count=self.queue.get())


thread = ParallelFunction()


def main():
    idleFns = []  # list of functions to call when gui is idle
    idleFns.append(onIdle)

    try:
        thread.start()

        print('starting event loop')
        eventLoop = True
        while eventLoop:
            time.sleep(1)  # pretending the main thread stuff is doing some stuff
            for idleFn in idleFns:
                idleFn()

    except KeyboardInterrupt:
        print('Main interrupted, stopping the auxillary thread')
        thread.stop()

    except Exception as exc:
        exc = sys.exc_info()[1]
        print(exc)
        print('Exception, stopping auxillary thread')
        thread.stop()


if __name__ == "__main__":
    main()
