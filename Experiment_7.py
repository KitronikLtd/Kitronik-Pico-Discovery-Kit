import machine
import utime
import _thread

#Setup 2 digital inputs for buttons
ButtonA  = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
ButtonB  = machine.Pin(1,machine.Pin.IN, machine.Pin.PULL_DOWN)
                      
#Setup 6 digital outputs to drive LEDs 
Red = machine.Pin(10,machine.Pin.OUT) 
Yellow = machine.Pin(11,machine.Pin.OUT) 
Green = machine.Pin(12,machine.Pin.OUT) 
PedestrianRed = machine.Pin(6,machine.Pin.OUT)
PedestrianWait = machine.Pin(7,machine.Pin.OUT)
PedestrianGreen = machine.Pin(8,machine.Pin.OUT)

#Setup a PWM Output for the beeping of a crossing
Buzzer = machine.PWM(machine.Pin(15)) 
Buzzer.duty_u16(0) #Start with the buzzer off
Frequency = 1000  #set a frequency of 1 Khz

#Control Variable 
CrossRequested = False

#This is a thread that takes care of beeping the buzzer

def PedestrianCross():
    global CrossRequested
    PedestrianRed(0)
    PedestrianGreen(1)
    PedestrianWait(0)
    OnTime = 50
    print ("Beeping")
    for Beeping in range (10):
        Buzzer.duty_u16(32767)
        utime.sleep_ms(OnTime)
        Buzzer.duty_u16(0)
        utime.sleep_ms(1000-OnTime)
    print("End Beep Thread")
    PedestrianRed(1)
    PedestrianGreen(0)
    CrossRequested = False

#Only set the request flag once - if its already set we 
#just exit the IRQ. 
#We dont need to check who asked for the cross, it does 
#the same for both “sides” of the road - either Button 

def ButtonIRQHandler(pin):
    global CrossRequested
    if CrossRequested == False:
        print ("Button Pressed")
        CrossRequested = True
        PedestrianWait.value(1) #Indicate to wait.


#setup the IRQ and hook it to the handler
ButtonA.irq(trigger = machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   
ButtonB.irq(trigger = machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   

#Setup the intial Light states  - 
#Road stopped, pedestrian stopped, wait off.
Red.value(1)
Yellow.value(0)
Green.value(0)
PedestrianRed.value(1)
PedestrianGreen.value(0)
PedestrianWait.value(0)
#this sleep here is so the start set of Red occurs
utime.sleep(2)

#The main loop runs the LEDS one and off. 
while True:
    #We start with the Traffic Lights on Stop, 
    #so check if anyone wants to cross
    if CrossRequested == True:
        _thread.start_new_thread(PedestrianCross,())
        #Now hang around until the pedestrian is done.
        while CrossRequested:
            utime.sleep(1)
    else: #drive the traffic light sequence
        Yellow.value(1)
        utime.sleep(1)
        Red.value(0)
        Yellow.value(0)
        Green.value(1)
        utime.sleep(2)
        Yellow.value(1)
        Green.value(0)
        utime.sleep(1)
        Red.value(1)
        Yellow.value(0)
        utime.sleep(2)
