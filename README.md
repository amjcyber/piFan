# piFan
This is a small project to play a bit with RaspberryPi, IR and my fan.
The aim is to be able to automate my fan.

## What we need
- RaspberryPi
- Jump wires
- 1 red LED
- 1 PN2222 transistor
- 1 680 ohm resistor
- 1 220 ohm resistor
- 1 infrared receiver
- 1 infrared LED
- Bread board

## The circuits

### IR Receiver

### IR Sender

## Recording IR signal
We will use [PiIR](https://github.com/ts1/PiIR) that is based on [PiGPIO](http://abyz.me.uk/rpi/pigpio/) a much better, easy to use and modern way to deal with IR from RPi than LIRC.

Record:
```
piir record --gpio <Your-GPIO-PIN> --file record.json
```
Once recorded we will use the `record.json` directly from the python web app.

## Web App
The web app is based on python flask. For scheduling the actions (turn on, turn off, set high speed for fan...) we use the native Linux Cron.
At the end, it's and extremely simple and easy to read app so you can modify if for whatever you want. It's just a demostration of how we can automate any IR-based system.