import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
count = 0

def get_RG11() -> float:
    """
    Gets the amount of rainfall since the last reset

    Arguments: None

    Returns: The amount of water fallen in mm
    """
    return round(count*0.2, 2)

def reset_RG11():
    """
    Resets the counter

    Arguments: None

    Returns: None
    """
    global count
    count = 0

def button_callback(channel):
    """
    Callback function to increase the rainfall counter for the RG11
    
    Arguments:
        - channel: the callback channel

    Returns: None
    """
    global count
    count += 1


def RG11():

    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(10, GPIO.FALLING, callback=button_callback, bouncetime=115) # Setup event on pin 10 rising edge

    while True:
        sleep(3)

    GPIO.cleanup()


def is_any_thread_alive(threads):
    """
    Checks if there are any threads running

    Arguments:
        - threads: A list of threads running

    returns: True if there are any live threads, False otherwise
    """
    return True in [t.is_alive() for t in threads]

def main():
    """
    Driver function
    """
    import threading
    run_RG11 = threading.Thread(target=RG11, name="RG11", daemon=True)
    run_RG11.start()
    
    while is_any_thread_alive([run_RG11]):
        print("Rainfall: " + str(get_RG11()) + "mm")
        sleep(3)

if __name__ == '__main__':
    main()