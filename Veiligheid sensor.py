from machine import Pin, time_pulse_us
import time
import neopixel
import socket
 
np = neopixel.NeoPixel(machine.Pin(28), 8)
trigger_pin = Pin(17, Pin.OUT)
echo_pin = Pin(13, Pin.IN)
 
def measure_distance():
    """Meet de afstand met de SR04."""
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(10)
    trigger_pin.low()
 
    pulse_duration = time_pulse_us(echo_pin, 1, 30000)
    distance = (pulse_duration / 2) / 29.1  # Afstand in cm
    return distance

def display_distance(distance):
    """Laat de afstand d.m.v. de leds zien."""
    if distance >= 100:
        np.fill((0, 0, 0)) 
    elif distance >= 50:
        np.fill((0, 255, 127)) 
    elif distance >= 20:
        np.fill((0, 255, 0)) 
    elif distance >= 10:
        np.fill((255, 127, 0)) 
    elif distance >=0:
        np.fill((255, 0, 0))
    else:
        np.fill((0, 0, 0))  # Uit als afstand kleiner is dan 10 cm
 
    np.write()  # Update de LEDs slechts één keer!
 
while True:
    distance = measure_distance()
    print(f'Afstand gemeten: {distance:.2f} cm')
    display_distance(distance)
    time.sleep_ms(100)
