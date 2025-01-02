import board
import digitalio
import adafruit_ssd1306
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import time

class DigitalPet:
    def __init__(self):
        # Initialize I2C and OLED
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        
        # Clear display
        self.oled.fill(0)
        self.oled.show()
        
        # Create blank image for drawing
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        
        # Button setup
        GPIO.setmode(GPIO.BCM)
        # Define your button pins here
        self.FEED_BTN = 17    # Example GPIO pin
        self.PET_BTN = 27     # Example GPIO pin
        self.PLAY_BTN = 22    # Example GPIO pin
        
        # Setup buttons with pull-down resistors
        GPIO.setup(self.FEED_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PLAY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Pet stats
        self.hunger = 100
        self.happiness = 100
    
    def test_display(self):
        """Test function to verify OLED display is working"""
        # Draw some test text
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        self.draw.text((0, 0), "Display Test!", fill=255)
        self.draw.text((0, 20), "Digital Pet", fill=255)
        
        # Show the image
        self.oled.image(self.image)
        self.oled.show()
    
    def test_buttons(self):
        """Test function to verify buttons are working"""
        print("Press each button to test (Ctrl+C to exit):")
        try:
            while True:
                if GPIO.input(self.FEED_BTN):
                    print("Feed button pressed!")
                    time.sleep(0.2)  # Debounce
                if GPIO.input(self.PET_BTN):
                    print("Pet button pressed!")
                    time.sleep(0.2)  # Debounce
                if GPIO.input(self.PLAY_BTN):
                    print("Play button pressed!")
                    time.sleep(0.2)  # Debounce
        except KeyboardInterrupt:
            print("\nButton test complete!")
    
    def cleanup(self):
        """Clean up GPIO on exit"""
        GPIO.cleanup()

def main():
    pet = DigitalPet()
    
    # Test display
    print("Testing OLED display...")
    pet.test_display()
    time.sleep(2)
    
    # Test buttons
    print("Testing buttons...")
    pet.test_buttons()
    
    # Cleanup
    pet.cleanup()

if __name__ == "__main__":
    main()