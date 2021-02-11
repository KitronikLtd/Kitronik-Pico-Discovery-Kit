import machine

#Setup 2 digital outputs to drive LEDs 
LED1 = machine.Pin(25,machine.Pin.OUT)
LED2 = machine.Pin(10,machine.Pin.OUT)

#Setup 2 digital inputs for buttons
ButtonA  = machine.Pin(0, machine.Pin.IN, 
                       machine.Pin.PULL_DOWN)
ButtonB  = machine.Pin(1,machine.Pin.IN,
                       machine.Pin.PULL_DOWN)

#initialise the LEDs as ‘Off’                       
LEDState1 = False
LEDState2 = False

#These IRQ Handlers toggle the variables we use to light 
#the LEDs. They check which pin caused the IRQ so 1 button
#controls the onboard LED and the other button controls 
#the breadboard LED

def ButtonAIRQHandler(pin):
    global LEDState1 
    if pin == ButtonA:
        if LEDState1 == True:
            LEDState1 = False
        else:
            LEDState1 = True

def ButtonBIRQHandler(pin):
      global LEDState2 
      if pin == ButtonB:
        if LEDState2 == True:
            LEDState2 = False
        else:
            LEDState2 = True
     
#setup the IRQ and hook it to the handler
ButtonA.irq(trigger = machine.Pin.IRQ_RISING, 
            handler =  ButtonAIRQHandler)   
ButtonB.irq(trigger = machine.Pin.IRQ_RISING, 
            handler =  ButtonBIRQHandler)   

#now loop and light each LED with its LED State
while True:
    LED1.value(LEDState1)
    LED2.value(LEDState2)
