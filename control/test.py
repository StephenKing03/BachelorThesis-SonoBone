import stepper_control as sc
import time

sc.init_steppers()
sc.wait_done()
sc.turn_base(30, 0)
time.sleep(0.05)
sc.turn_base(60, 1)
print("-----------wait Nr0")
sc.wait_done_base(30, 0)
print("------------NR0 done")
time.sleep(0.05)
sc.turn_base(30, 2)
print("-----------wait Nr1")
sc.wait_done_base(60, 1)
print("------------NR1 done")

sc.wait_done_base(30,2)
print("------------NR2 done")