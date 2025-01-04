import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time
import random
import threading

class DigitalPet:
    def __init__(self):
        # Initialize I2C and OLED
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        
        # Create blank image for drawing
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        
        # Button setup
        GPIO.setmode(GPIO.BCM)
        self.FEED_BTN = 17
        self.PET_BTN = 27
        self.PLAY_BTN = 22
        GPIO.setup(self.FEED_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PET_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PLAY_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Pet stats and state
        self.hunger = 100
        self.happiness = 100
        self.is_sleeping = False
        self.last_interaction = time.time()
        self.animation_frame = 0
        self.scroll_position = 0
        self.last_update = time.time()
        
        # Constants
        self.SLEEP_TIMEOUT = 120  # 2 minutes (changed from 300)
        self.HUNGER_DECAY = 5     # per minute
        self.HAPPINESS_DECAY = 7   # per minute
        self.running = True
        
        # Bunny ASCII frames for different states
        self.bunny_normal = [
            """ (\_/)
 (•ᴥ•)
(")_(")""",
            """ (\_/)
 (•ᴥ•)
(")^(")"""
        ]
        
        self.bunny_happy = [
            """ (\_/)
 (^ᴥ^)
(")_(")""",
            """ (\_/)
 (^ᴥ^)
(")^(")"""
        ]
        
        self.bunny_sad = [
            """ (\_/)
 (•︵•)
(")_(")""",
            """ (\_/)
 (•︵•)
(")^(")"""
        ]

        self.bunny_sleeping = [
            """   (\ /)
  (- . -)
  ("|"|)""",
            """   (\ /)
  (- . -)
   ("|"|)"""
        ]
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self.animate, daemon=True)
        self.animation_thread.start()

    def animate(self):
        """Animation loop running in separate thread"""
        while self.running:
            self.animation_frame = (self.animation_frame + 1) % 2
            if self.is_sleeping:
                self.scroll_position = (self.scroll_position + 2) % self.oled.width  # Doubled scroll speed
                time.sleep(0.25)  # Faster animation when sleeping
            else:
                time.sleep(0.5)  # Normal animation speed

    def update_stats(self):
        """Update pet stats based on time passed"""
        current_time = time.time()
        minutes_passed = (current_time - self.last_update) / 60.0
        
        # Calculate decay
        hunger_loss = self.HUNGER_DECAY * minutes_passed
        happiness_loss = self.HAPPINESS_DECAY * minutes_passed
        
        # Update stats with limits
        self.hunger = max(0, min(100, self.hunger - hunger_loss))
        self.happiness = max(0, min(100, self.happiness - happiness_loss))
        
        self.last_update = current_time
    
    def get_mood(self):
        """Determine pet's mood based on stats"""
        avg_state = (self.hunger + self.happiness) / 2
        if avg_state > 75:
            return "Happy!"
        elif avg_state > 50:
            return "Content"
        elif avg_state > 25:
            return "Unhappy"
        else:
            return "Miserable"
    
    def draw_bunny(self):
        """Draw the bunny in current state"""
        mood = self.get_mood()
        bunny_frames = self.bunny_normal
        
        if self.is_sleeping:
            # Draw scrolling ZZZs
            zzz_text = "z Z z Z z Z"
            text_width = len(zzz_text) * 8  # Approximate width
            x_pos = self.oled.width - self.scroll_position
            # Center the ZZZs vertically
            self.draw.text((x_pos, self.oled.height // 3), zzz_text, fill=255)
            if x_pos < -text_width:
                self.scroll_position = 0
        else:
            # Draw appropriate bunny frame
            if mood == "Happy!":
                bunny_frames = self.bunny_happy
            elif mood in ["Unhappy", "Miserable"]:
                bunny_frames = self.bunny_sad
            
            # Center the bunny horizontally and lower vertically
            text_width = 32  # Approximate width of bunny ASCII art
            x_pos = ((self.oled.width - text_width) // 2) + 8  # Added 8 pixels (about one space) to move right
            y_pos = 20  # Lower position to make room for status bars
            self.draw.text((x_pos, y_pos), bunny_frames[self.animation_frame], fill=255)
    
    def check_sleep(self):
        """Check if pet should sleep"""
        if time.time() - self.last_interaction > self.SLEEP_TIMEOUT:
            if not self.is_sleeping:
                print("Pet is going to sleep...")
                self.is_sleeping = True
        else:
            self.is_sleeping = False
    
    def handle_buttons(self):
        """Handle button inputs"""
        if self.is_sleeping:
            # Any button press wakes up the pet
            if any([GPIO.input(self.FEED_BTN), GPIO.input(self.PET_BTN), GPIO.input(self.PLAY_BTN)]):
                self.is_sleeping = False
                self.last_interaction = time.time()
                print("Pet woke up!")
                return
        
        if GPIO.input(self.FEED_BTN):
            print("Feeding pet!")
            self.hunger = min(100, self.hunger + 15)
            self.last_interaction = time.time()
            time.sleep(0.2)
            
        if GPIO.input(self.PET_BTN):
            print("Petting!")
            self.happiness = min(100, self.happiness + 15)
            self.last_interaction = time.time()
            time.sleep(0.2)
            
        if GPIO.input(self.PLAY_BTN):
            print("Playing!")
            self.hunger = max(0, self.hunger - 5)
            self.happiness = min(100, self.happiness + 10)
            self.last_interaction = time.time()
            time.sleep(0.2)
    
    def check_random_events(self):
        """Generate random events"""
        if random.random() < 0.01 and not self.is_sleeping:  # 1% chance per check
            self.hunger = max(0, self.hunger - 20)  # Sudden hunger
            print("Pet is suddenly hungry!")
    
    def draw_status_bar(self, y_pos, value, label):
        """Draw a dashed status bar"""
        # Draw label
        label_with_padding = f"{label}:  "  # Added extra space after colon
        self.draw.text((0, y_pos), label_with_padding, fill=255)
        
        # Calculate bar position (starting after label)
        bar_start_x = 45  # Adjusted to align bars while accommodating longer "Hunger" label
        dash_length = 4
        gap_length = 3
        dash_height = 4
        total_dashes = 12
        
        # Calculate how many dashes should be filled based on value
        filled_dashes = int((value / 100.0) * total_dashes)
        
        # Draw dashes
        for i in range(total_dashes):
            x_pos = bar_start_x + i * (dash_length + gap_length)
            if i < filled_dashes:
                # Filled dash - solid white rectangle
                self.draw.rectangle(
                    (x_pos, y_pos + 2, x_pos + dash_length - 1, y_pos + dash_height + 1),
                    outline=255,
                    fill=255
                )
            else:
                # Empty dash - just a single line
                self.draw.line(
                    (x_pos, y_pos + 4, x_pos + dash_length - 1, y_pos + 4),
                    fill=255,
                    width=1
                )

    def update_display(self):
        """Update OLED display"""
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        # Draw status bars at top if not sleeping
        if not self.is_sleeping:
            self.draw_status_bar(0, self.hunger, "Hunger")
            self.draw_status_bar(8, self.happiness, "Happy")
        
        # Draw bunny
        self.draw_bunny()
        
        self.oled.image(self.image)
        self.oled.show()

    def run(self):
        """Main loop"""
        print("Digital Pet is running! Press Ctrl+C to exit")
        try:
            while self.running:
                self.update_stats()
                self.check_sleep()
                self.handle_buttons()
                self.check_random_events()
                self.update_display()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO and clear display"""
        self.running = False
        self.oled.fill(0)
        self.oled.show()
        GPIO.cleanup()
        print("\nGoodbye!")

if __name__ == "__main__":
    pet = DigitalPet()
    pet.run()