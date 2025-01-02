import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time

class DigipetTest:
    def __init__(self):
        # Initialize I2C and OLED
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        
        # Create blank image for drawing
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        
        # Button setup
        GPIO.setmode(GPIO.BCM)
        self.FEED_BTN = 17    # Pin 11
        self.PET_BTN = 27     # Pin 13
        self.PLAY_BTN = 22    # Pin 15
        
        # Setup buttons with pull-down configuration
        GPIO.setup(self.FEED_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PLAY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def update_display(self, text_lines):
        """Update OLED with new text"""
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        y_position = 0
        for line in text_lines:
            self.draw.text((0, y_position), line, fill=255)
            y_position += 12
        self.oled.image(self.image)
        self.oled.show()
    
    def run_test(self):
        """Run the combined OLED and button test"""
        try:
            # Initial display
            self.update_display([
                "Button Test",
                "Press buttons:",
                "1: Feed",
                "2: Pet",
                "3: Play"
            ])
            
            while True:
                if GPIO.input(self.FEED_BTN):
                    self.update_display([
                        "Feed button (GPIO17)",
                        "Pin 11 pressed!"
                    ])
                    print("Feed button (GPIO17/Pin 11) pressed!")
                    time.sleep(0.3)  # Increased debounce time
                
                if GPIO.input(self.PET_BTN):
                    self.update_display([
                        "Pet button (GPIO27)",
                        "Pin 13 pressed!"
                    ])
                    print("Pet button (GPIO27/Pin 13) pressed!")
                    time.sleep(0.3)  # Increased debounce time
                
                if GPIO.input(self.PLAY_BTN):
                    self.update_display([
                        "Play button (GPIO22)",
                        "Pin 15 pressed!"
                    ])
                    print("Play button (GPIO22/Pin 15) pressed!")
                    time.sleep(0.3)  # Increased debounce time
                
        except KeyboardInterrupt:
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO and clear display"""
        self.oled.fill(0)
        self.oled.show()
        GPIO.cleanup()
        print("\nTest complete!")

if __name__ == "__main__":
    test = DigipetTest()
    test.run_test()