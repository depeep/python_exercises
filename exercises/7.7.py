
import time

class Stopwatch:
    def __init__(self):
        self.__startTime = time.time()
        self.__endTime = time.time()

    def start(self):
        self.__startTime = time.time()


    def stop(self):   
        self.__endTime = time.time()

 
    def getElapsedTime(self):
        start = self.__startTime
        end = self.__endTime
        elapsed = end - start
        return elapsed

def main():
    myStopwatch = Stopwatch()
    myStopwatch.start()
    time.sleep (5)
    myStopwatch.stop()
    print(myStopwatch.getElapsedTime())
    time.sleep(10)
    myStopwatch.stop()
    print(myStopwatch.getElapsedTime())
    time.sleep(5)
    print(myStopwatch.getElapsedTime())


if __name__ ==  "__main__":
    main()

    
