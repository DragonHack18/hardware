# External module imports
import RPi.GPIO as GPIO
import time
import urllib.request

# Pin Definitons:
pwmPin = 18  # Broadcom pin 18 (P1 pin 12)
ledPin = 14  # Broadcom pin 23 (P1 pin 16)
butPin = 17  # Broadcom pin 17 (P1 pin 11)

dc = 95  # duty cycle (0-100) for PWM pin


def clean():
    pwm.stop()  # stop PWM
    GPIO.cleanup()  # cleanup all GPIO


def blink_once():
    pwm.ChangeDutyCycle(100 - dc)
    GPIO.output(ledPin, GPIO.HIGH)
    time.sleep(0.075)
    GPIO.output(ledPin, GPIO.LOW)
    time.sleep(0.075)


# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT)  # LED pin set as output
GPIO.setup(pwmPin, GPIO.OUT)  # PWM pin set as output
pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)
pwm.start(dc)

# servo init

servoPin = 2

GPIO.setup(servoPin, GPIO.OUT)


def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)


# end servo init

print("Here we go! Press CTRL+C to exit")
try:

    INIT_TIME = time.time()

    while 1:
        pwm.start(0)
        print("debug point 1")
        SetAngle(90)
        print("debug point 2")
        print("GPIO button: " + str(GPIO.input(butPin)))

        blink_once()
        if GPIO.input(butPin) < 1:  # button is pressed
            print("debug button point 1")
            contents = urllib.request.urlopen("http://localhost/dragonhack/public/index.php/api/approvepayment").read()
            clean()
            exit()

        if time.time() - INIT_TIME > 10:
            print("debug time point 1")
            clean()
            exit()


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print("debug exception point 1")
    clean()

except Exception as e:
    print(e)
    print("debug exception point 2")
    clean()
