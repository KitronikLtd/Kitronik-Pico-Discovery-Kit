import machine

#Setup 2 digital inputs for buttons
ButtonA  = machine.Pin(0, machine.Pin.IN, 
                       machine.Pin.PULL_DOWN)
ButtonB  = machine.Pin(1,machine.Pin.IN,
                       machine.Pin.PULL_DOWN)
#setup a PWM Output
Buzzer = machine.PWM(machine.Pin(15)) 
Buzzer.duty_u16(32767) #make it 50% duty cycle (32767/65535)
Frequency = 1000  #set a starting frequency of 1 Khz

def ButtonIRQHandler(pin):
    global Frequency
    if pin == ButtonA: #up the frequency
        if Frequency < 2000:
            Frequency += 50
    elif pin == ButtonB: #lower the frequency
        if Frequency > 100:
            Frequency -= 50

#setup the IRQ and hook it to the handler
ButtonA.irq(trigger = machine.Pin.IRQ_RISING,
            handler =  ButtonIRQHandler)   
ButtonB.irq(trigger = machine.Pin.IRQ_RISING, 
            handler =  ButtonIRQHandler)   

while True:
    Buzzer.freq(Frequency)
