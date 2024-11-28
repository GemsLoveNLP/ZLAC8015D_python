from zlac8015d import ZLAC8015D
import keyboard
import time
import os

RPM = 15
RPM_DICT = {"w":[-RPM,RPM],
            "a":[RPM,RPM],
            "s":[RPM,-RPM],
            "d":[-RPM,-RPM]}


def connect_motors():
        
    ports = os.popen('ls /dev/ttyUSB*').read().strip().split("\n")
    motors_lst = []

    for port in ports:
        motors = ZLAC8015D.Controller(port=port)

        motors.disable_motor()

        motors.set_accel_time(1000,1000)
        motors.set_decel_time(1000,1000)

        motors.set_mode(3)
        motors.enable_motor()

        motors_lst.append((port,motors))

    return motors_lst

def main():
    motors_lst = connect_motors()
    try:
        last_time = time.time()
        for port, motors in motors_lst:
            motors.set_rpm(0, 0)
        while True:
            # get keyboard input
            key = input("Enter Key:").lower()

            if key in RPM_DICT:
                cmds = RPM_DICT[key]
                for port, motors in motors_lst:
                    motors.set_rpm(cmds[0], cmds[1])
            else:
                print("Turning off motors and exiting...")
                for port, motors in motors_lst:
                    motors.disable_motor()
                return

            # report speed
            for port, motors in motors_lst:
                rpmL, rpmR = motors.get_rpm()
                period = time.time() - last_time
                print("Port: {}, Period: {:.4f} rpmL: {:.1f} | rpmR: {:.1f}".format(port, period, rpmL, rpmR))

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) gracefully
        print("Keyboard interrupt detected. Disabling motors...")
        for port, motors in motors_lst:
            motors.disable_motor()

    except Exception as e:
        # Call disable_motor() in case of error
        print(f"An error occurred: {e}")
        for port, motors in motors_lst:
            motors.disable_motor()

if __name__ == "__main__":
    main()