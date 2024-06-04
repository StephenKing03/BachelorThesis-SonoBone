import stepper_control as sc
import time
from globals import GlobalState
import threading



sc.init_steppers()
sc.wait_init()

time.sleep(2)
sc.send_combined_position(30, 30, 1)

while sc.done_arduino(1) == False:
    time.sleep(0.01)

print("prgram done")
