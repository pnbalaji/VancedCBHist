import pyperclip
import time
import random
import string

for i in range(10):
    randstr = ''.join([random.choice(string.ascii_letters) for i in range(20)])
    print(i, randstr)
    pyperclip.copy(randstr)
    time.sleep(0.25)
