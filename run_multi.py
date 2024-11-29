from zlac8015d import ZLAC8015D
import keyboard
import time
import os

RPM = 250
RPM_DICT = {"w":[-RPM,RPM],
            "a":[RPM,RPM],
            "s":[RPM,-RPM],
            "d":[-RPM,-RPM],
            "x":[0,0]}


def connect_motors():

    # TODO: maybe add a check
    # !: any USB devices might show up here as well. We may need a way to detect that
        
    ports = os.popen('ls /dev/ttyUSB*').read().strip().split("\n")
    motors_lst = []

    for port in ports:
        motors = ZLAC8015D.Controller(port=port)

        motors.disable_motor()

        motors.set_accel_time(1000,1000)
        motors.set_decel_time(1000,1000)

        motors.set_mode(3)
        motors.enable_motor()

        l_tick_i, r_tick_i = motors.get_wheels_tick()

        motors_lst.append((port,motors,l_tick_i,r_tick_i))

    return motors_lst

def main():
    motors_lst = connect_motors()
    try:
        last_time = time.time()
        for port, motors, l_tick_i,r_tick_i in motors_lst:
            motors.set_rpm(0, 0)
        while True:
            # get keyboard input
            key = input("Enter Key:").lower()

            if key in RPM_DICT:
                cmds = RPM_DICT[key]
                for port, motors, l_tick_i,r_tick_i in motors_lst:
                    motors.set_rpm(cmds[0], cmds[1])
            else:
                print("Turning off motors and exiting...")
                for port, motors, l_tick_i,r_tick_i in motors_lst:
                    motors.disable_motor()
                return

            # report speed
            for port, motors, l_tick_i,r_tick_i in motors_lst:
                rpmL, rpmR = motors.get_rpm()
                # TODO: add a check. If the speed flips by above some value, regulate it.
                l_tick, r_tick = motors.get_wheels_tick()
                l_tick -= l_tick_i
                l_tick *= -1 # ? this is to make sure that 
                r_tick -= r_tick_i
                period = time.time() - last_time
                print("Port: {}, Period: {:.4f} rpmL: {:.1f} | rpmR: {:.1f}".format(port, period, rpmL, rpmR))
                # motors.set_rpm(cmds[0],cmds[1])
                print("period: {:.4f} l_tick: {:.1f} | r_tick: {:.1f}".format(period,l_tick,r_tick))

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) gracefully
        print("Keyboard interrupt detected. Disabling motors...")
        for port, motors, l_tick_i,r_tick_i in motors_lst:
            motors.disable_motor()

    except Exception as e:
        # Call disable_motor() in case of error
        print(f"An error occurred: {e}")
        for port, motors, l_tick_i,r_tick_i in motors_lst:
            motors.disable_motor()

if __name__ == "__main__":
    main()