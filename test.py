import time

from utils import RepeatTimer


def dummyfn(msg="foo"):
    print(msg)


timer = RepeatTimer(1, dummyfn)
timer.start()
time.sleep(500)
timer.cancel()
