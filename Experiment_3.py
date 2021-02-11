import machine

#Setup the onboard LED Pin as an output
LED = machine.Pin(25,machine.Pin.OUT)
Button = machine.Pin(0,machine.Pin.IN,machine.Pin.PULL_DOWN)
LEDState = False

#This IRQ Handler toggles the variable we use to light the 
# LED. It should, but doesnt check which pin raised the IRQ,
# as we only have 1 pin wired.
def ButtonIRQHandler(pin):
    global LEDState 
    if LEDState == True:
        LEDState = False
    else:
        LEDState = True
 
#setup the IRQ and hook it to the handler
Button.irq(trigger = machine.Pin.IRQ_RISING,
           handler =  ButtonIRQHandler)   
          
#now loop and light the LED with the LED State
while True:
    LED.value(LEDState)
