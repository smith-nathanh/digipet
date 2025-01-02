import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# Set up GPIO17 with internal pull-down resistor
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Testing GPIO17 (Pin 11) with internal pull-down")
print("Press the button (Ctrl+C to exit)")
print("State should be 0 when not pressed, 1 when pressed")

try:
    last_state = GPIO.input(17)
    while True:
        current_state = GPIO.input(17)
        if current_state != last_state:
            if current_state:
                print("Button PRESSED (1)")
            else:
                print("Button RELEASED (0)")
            last_state = current_state
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nTest complete!")