import machine
import utime
import _thread

#Setup digital input for buttons
ButtonA  = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

#Setup 3 digital outputs to drive LEDs 
Red = machine.Pin(10,machine.Pin.OUT) 
Yellow = machine.Pin(11,machine.Pin.OUT) 
Green = machine.Pin(12,machine.Pin.OUT) 

#Setup a PWM Output
Buzzer = machine.PWM(machine.Pin(15)) 
Buzzer.duty_u16(0) #Start with the buzzer off
Frequency = 1000  #set a frequency of 1 Khz

#Control Variable 
Beeping = False

#This is the thread routine, which will beep the buzzer
def Beep():
    global Beeping
    OnTime = 50
    print (“Start Beeping Thread”)
    while Beeping:
        Buzzer.duty_u16(32767)
        utime.sleep_ms(OnTime)
        Buzzer.duty_u16(0)
        utime.sleep_ms(1000-OnTime)
    print(“End Beeping Thread”)
   
def ButtonAIRQHandler(pin):
    global Beeping
    if Beeping == False:
        print (“Start Beep”)
        Beeping = True
        _thread.start_new_thread(Beep,())
    else:
        Beeping = False  #this causes the thread to exit
        print(“Stop Beep”)

#setup the IRQ and hook it to the handler
ButtonA.irq(trigger = machine.Pin.IRQ_RISING, handler =  ButtonAIRQHandler)   

#The main loop runs the LEDs in a chase pattern
while True:
    Red.toggle()
    utime.sleep_ms(100)
    Yellow.toggle()
    utime.sleep_ms(100)
    Green.toggle()
    utime.sleep_ms(100)
