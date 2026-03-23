class TV:
    def __init__(self):
        self.channel = 1 # the TV has a channel between 1 and 120
        self.volumeLevel = 1 # the TV has a volume between 1 and 7
        self.on = False # the TV is On (True) or Off (False)

    def turnOn(self):
        self.on = True

    def turnOff(self):
        self.on = False

    def getChannel(self):
        return self.channel

    def setChannel(self, channel):
        if self.on and 0 < channel < 121: 
            self.channel = channel

    def channelUp(self):
        if self.channel <120:  # if self.on vergeten
            self.channel +=1
        # your code, the channel should go up by one,
        # if it stays between 1 and 120

    def channelDown(self):  
        if self.channel >1: # if self.on vergeten
            self.channel -=1

        # your code, the channel should go down by one,
        # if it stays between 1 and 120

    def getVolume(self):
        return self.volumeLevel

    def setVolume(self, volumeLevel):
        # your code, the volume must stay between 1 and 7
        if 0< volumeLevel < 8: # if self.on vergeten
            self.volumeLevel = volumeLevel

    def volumeUp(self):
        if self.volumeLevel <7: # if self.on vergeten
            self.volumeLevel +=1
        # your code, the volume should go up by one,
        # if it stays between 1 and 7

    def volumeDown(self):
        if self.volumeLevel >1: # if self.on vergeten
            self.volumeLevel -=1
        # your code, the volume should go down by one,
        # if it stays between 1 and 7

def main():
    tv1 = TV()
    tv1.turnOn()
    tv1.setChannel(30)
    tv1.setVolume(3)

    tv2 = TV()
    tv2.turnOn()
    tv2.channelUp()
    tv2.channelUp()
    tv2.volumeUp()

    print("tv1's channel is", tv1.getChannel(),
          "and volume level is", tv1.getVolume())
    print("tv2's channel is", tv2.getChannel(),
          "and volume level is", tv2.getVolume())

main() # call the main() function