# bestand om de waarden in config als uitprobeersel uit te lezen en aan te passen
import config

conf= config.Config()
max, visible, between = conf.getStartTestSettings()
print (max, "levels")
print (visible, "ms visible)" )
print (between, "ms between" )

print()
geometry, width, height, font =conf.getWindowConfig()
print ("Windowconfiguratie:")
print ("geometry", geometry)
print ("width",width)
print ("height",height)
print ("font",font)

print()
size = conf.getSize()
print ("size", size, "x", size)

conf.setSize(5)

print()
size = conf.getSize()
print ("size na set", size, "x", size)
