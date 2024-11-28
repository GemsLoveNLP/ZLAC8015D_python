from zlac8015d import ZLAC8015D
import time

RPM = 15
RPM_DICT = {"w":[-RPM,RPM],
            "a":[RPM,RPM],
            "s":[RPM,-RPM],
            "d":[-RPM,-RPM]}

def set_up():
    motors = ZLAC8015D.Controller(port="/dev/ttyUSB0")

    motors.disable_motor()

    motors.set_accel_time(1000,1000)
    motors.set_decel_time(1000,1000)

    motors.set_mode(3)
    motors.enable_motor()

    return motors

def main():
    motors = set_up()
    motors.set_rpm(0,0)
    last_time = time.time()

    while True:
        # time.sleep(0.01)

        key = input("Enter Key:").lower()
        
        if key in RPM_DICT:
            cmds = RPM_DICT[key]
            motors.set_rpm(cmds[0],cmds[1])

        else:
            motors.disable_motor()
            return
        
        rpmL, rpmR = motors.get_rpm()
        period = time.time() - last_time
        print("Period: {:.4f} rpmL: {:.1f} | rpmR: {:.1f}".format(period,rpmL,rpmR))
        
        


if __name__ == "__main__":
    main()