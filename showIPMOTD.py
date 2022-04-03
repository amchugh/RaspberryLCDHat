
# Small variation on the original showIP program :)

import LCD_1in44
import LCD_Config

import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont, ImageColor

KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16
BACKLIGHT = 24


def setupDisplay():
    # Init GPIO
    GPIO.setmode(GPIO.BCM)

    # Setup all of the keys - including the 'joystick' - to be in pull up mode.
    GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # 240x240 display with hardware SPI:
    disp = LCD_1in44.LCD()
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    disp.LCD_Init(Lcd_ScanDir)
    disp.LCD_Clear()
    return disp


def makeImage():
    # Create blank image for drawing.
    width = 128
    height = 128
    image = Image.new('RGB', (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Return the drawing object
    return image, draw


def getLocalIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        result = s.getsockname()[0]
    except Exception:
        result = '127.0.0.1'
    finally:
        s.close()
    return result


def drawIP(disp):
    localIP = getLocalIP()
    image, draw = makeImage()
    # Create font and put the IP address on the image
    font = ImageFont.truetype(
        '/home/ubuntu/screen/RaspberryLCDHat/VCR_OSD_MONO_1.001.ttf', 14)
    draw.text((5, 100), str(localIP), font=font, align="left")
    # Update the display with the image
    disp.LCD_ShowImage(image, 0, 0)


if __name__ == "__main__":
    print("Drawing IP to display...")
    disp = setupDisplay()
    drawIP(disp)
    print("Done.")
