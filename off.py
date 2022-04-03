
BACKLIGHT = 24

if __name__ == "__main__":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BACKLIGHT, GPIO.OUT)
    GPIO.output(BACKLIGHT, GPIO.LOW)
