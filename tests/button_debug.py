import RPi.GPIO as GPIO
import time

def test_single_button(pin, name):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    print(f"\nTesting {name} button on GPIO{pin}")
    print("Press the button several times (Ctrl+C to exit)")
    
    try:
        last_state = GPIO.input(pin)
        while True:
            current_state = GPIO.input(pin)
            if current_state != last_state:
                if current_state:
                    print(f"{name} button pressed! (GPIO{pin} HIGH)")
                else:
                    print(f"{name} button released! (GPIO{pin} LOW)")
                last_state = current_state
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{name} button test complete!")
        GPIO.cleanup()

# Test each button individually
while True:
    print("\nWhich button would you like to test?")
    print("1. Feed Button (GPIO17)")
    print("2. Pet Button (GPIO27)")
    print("3. Play Button (GPIO22)")
    print("4. Exit")
    
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        test_single_button(17, "Feed")
    elif choice == '2':
        test_single_button(27, "Pet")
    elif choice == '3':
        test_single_button(22, "Play")
    elif choice == '4':
        print("Test complete!")
        break
    else:
        print("Invalid choice. Please try again.")