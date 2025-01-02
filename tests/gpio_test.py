import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

print("Testing GPIO17 (Pin 11)")
print("Reading pin state every second for 10 seconds...")

try:
    for i in range(10):
        state = GPIO.input(17)
        print(f"GPIO17 state: {state}")
        time.sleep(1)
finally:
    GPIO.cleanup()
    print("Test complete!")