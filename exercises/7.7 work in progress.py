from datetime import datetime
from datetime import time
import time

class Stopwatch:
    def __init__(self):
        self.__startTime = datetime.now().time()
        self.__endTime = datetime.now().time()

    def start(self):
        self.__startTime = datetime.now().time()


    def stop(self):   
        self.__endTime = datetime.now().time()

 
    def getElapsedTime(self):
        start = int(self.__startTime())
        end = int(self.__endTime())
        elapsed = end - start
        return elapsed

def main():
    myStopwatch = Stopwatch()
    myStopwatch.start()
    time.sleep (5)
    myStopwatch.stop()
    print(myStopwatch.getElapsedTime())
    sleep(5)
    print(myStopwatch.getElapsedTime())


if __name__ ==  "__main__":
    main()

    
