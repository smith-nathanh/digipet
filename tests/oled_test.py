import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Create the I2C interface
i2c = board.I2C()

# Create the OLED class (explicitly setting address to 0x3C)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw a test pattern
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
draw.text((0, 0), "Success!", fill=255)
draw.text((0, 20), "OLED is working!", fill=255)
draw.rectangle((0, 40, 127, 50), outline=255, fill=0)

# Display image
oled.image(image)
oled.show()

print("If you can see text on the OLED display, the test was successful!")
print("Press Ctrl+C to exit")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    # Clear the display on exit
    oled.fill(0)
    oled.show()
    print("\nTest complete!")