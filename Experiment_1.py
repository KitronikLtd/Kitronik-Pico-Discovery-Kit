import machine
import utime

#Setup the onboard LED Pin as an output
LED = machine.Pin(25,machine.Pin.OUT) 

while True:
    LED.value(1)
    utime.sleep_ms(500)
    LED.value(0)
    utime.sleep_ms(500)
