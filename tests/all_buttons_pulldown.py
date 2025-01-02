import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Define pins for each button
FEED_BTN = 17  # Pin 11
PET_BTN = 27   # Pin 13
PLAY_BTN = 22  # Pin 15

# Setup all buttons with internal pull-down resistors
GPIO.setup(FEED_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PLAY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Testing all three buttons (Ctrl+C to exit)")
print("FEED: GPIO17 (Pin 11)")
print("PET:  GPIO27 (Pin 13)")
print("PLAY: GPIO22 (Pin 15)")

try:
    # Track last state of each button
    last_states = {
        FEED_BTN: GPIO.input(FEED_BTN),
        PET_BTN: GPIO.input(PET_BTN),
        PLAY_BTN: GPIO.input(PLAY_BTN)
    }
    
    while True:
        # Check each button
        for btn, name in [(FEED_BTN, "FEED"), (PET_BTN, "PET"), (PLAY_BTN, "PLAY")]:
            current_state = GPIO.input(btn)
            if current_state != last_states[btn]:
                if current_state:
                    print(f"{name} button PRESSED")
                else:
                    print(f"{name} button RELEASED")
                last_states[btn] = current_state
        
        time.sleep(0.1)  # Small delay to prevent CPU overload

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nTest complete!")