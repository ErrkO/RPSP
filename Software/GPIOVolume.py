# GPIO support import definition
import RPI.GPIO as GPIO
# External support for calling a process
import subproccess

#####################
#  Pin Definitions  #
#####################

VolUpPin
VolDwnPin
VolMtPin

# Amixer min and max volume numbers
MIN = 0
MAX = 200

###############
#  Pin Setup  #
###############

# Setting the pin mode to read the broadcom chip definitions
GPIO.setmode(GPIO.BCM)
# Setup for the individual pins
GPIO.setup( VolUpPin, GPIO.IN, pull_up_down=GPIO.PUD_UP )
GPIO.setup( VolDwnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP )
GPIO.setup( VolMtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP )

##############
#  Defaults  #
##############

# The initial state of the mute button
isMuted = False
# The initial volume position, halfway point
preVol = volume = 100

subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])

##############
#  The Loop  #
##############

try:

    while True:

        upPushed = GPIO.input(VolUpPin)
        downPushed = GPIO.input(VolDwnPin)
        mutePushed = GPIO.input(VolMtPin)

        if mutePushed:

            if isMuted:

                volume = PreVol
                isMuted = False
                print "Unmuted"

            else:

                PreVol = volume
                volume = MIN
                isMuted = True
                print "Muted"

            subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])

        else:

            if upPushed and not downPushed:

                if isMuted:

                    isMuted = False
                    volume = MIN

                else:

                    volume += 20

                    if volume > MAX:

                        volume = MAX

            if not upPushed and downPushed:

                if isMuted:

                    isMuted = False
                    volume = MIN

                else:

                    volume -= 20

                    if volume < MIN:

                        volume = MIN

            print "{:d} ({:.0%})".format(volume, float(volume)/float(max))
            subprocess.call(['amixer', '-q', '-c', '0', 'cset', 'numid=1', str(volume)])

finally:

    GPIO.cleanup()