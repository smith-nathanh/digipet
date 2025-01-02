import RPi.GPIO as GPIO
import time

# Clean up any previous configurations
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
# Set up GPIO17 with internal pull-down resistor
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Testing GPIO17 (Pin 11) with internal pull-down")
print("Default state should be 0")
print("Reading pin state every second for 10 seconds...")

try:
    for i in range(10):
        state = GPIO.input(17)
        print(f"GPIO17 state: {state}")
        time.sleep(1)
finally:
    GPIO.cleanup()
    print("Test complete!")