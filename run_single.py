from zlac8015d import ZLAC8015D
import keyboard
import time

RPM = 2
RPM_DICT = {"w":[-RPM,RPM],
            "a":[RPM,RPM],
            "s":[RPM,-RPM],
            "d":[-RPM,-RPM]}

def connect_motors():
    motors = ZLAC8015D.Controller(port=f"/dev/ttyUSB{input('USB: ')}")

    motors.disable_motor()

    motors.set_accel_time(1000,1000)
    motors.set_decel_time(1000,1000)

    motors.set_mode(3)
    motors.enable_motor()

    return motors

def main():
    motors = connect_motors()
    try:
        motors.set_rpm(0, 0)
        last_time = time.time()

        while True:
            # get keyboard input
            key = input("Enter Key:").lower()

            if key in RPM_DICT:
                cmds = RPM_DICT[key]
                motors.set_rpm(cmds[0], cmds[1])
            else:
                print("Turning off motors and exiting...")
                motors.disable_motor()
                return

            # report speed
            rpmL, rpmR = motors.get_rpm()
            period = time.time() - last_time
            print("Period: {:.4f} rpmL: {:.1f} | rpmR: {:.1f}".format(period, rpmL, rpmR))

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) gracefully
        print("Keyboard interrupt detected. Disabling motors...")
        motors.disable_motor()

    except Exception as e:
        # Call disable_motor() in case of error
        print(f"An error occurred: {e}")
        motors.disable_motor()

if __name__ == "__main__":
    main()