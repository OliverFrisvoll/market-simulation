import time
import datetime

print(start := datetime.datetime.now())

time.sleep(5)

print(end := datetime.datetime.now())

print((end - start).days / 365)
