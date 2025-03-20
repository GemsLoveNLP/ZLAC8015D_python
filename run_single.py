from zlac8015d import ZLAC8015D
import keyboard
import time

RPM = 30
RPM_DICT = {"w":[-RPM,RPM],
            "a":[RPM,RPM],
            "s":[RPM,-RPM],
            "d":[-RPM,-RPM],
            "x":[0,0]}


def connect_motors():
    motors = ZLAC8015D.Controller(port=f"/dev/ttyUSB0")

    motors.disable_motor()

    x = 100
    motors.set_accel_time(x,x)
    motors.set_decel_time(x,x)

    motors.set_mode(3)
    motors.enable_motor()

    return motors

# def get_tick(motors):
#     l_tick, r_tick = motors.get_wheels_tick()
#     return l_tick, r_tick

def main():
    motors = connect_motors()
    try:
        motors.set_rpm(0, 0)
        last_time = time.time()

        L_TICK, R_TICK = motors.get_wheels_tick()
        D_L, D_R = motors.get_wheels_travelled()
        print(f"Initial l_tick: {L_TICK}, r_tick: {R_TICK}")
        print(f"Initial D_L: {D_L}, D_R: {D_R}")
        old_l_tick, old_r_tick = L_TICK, R_TICK
        old_dl, old_dr = D_L, D_R

        # cmds = RPM_DICT["w"]
        # motors.set_rpm(cmds[0], cmds[1])
        # print(motors.get_wheels_travelled())

        # time.sleep(120)
        
        # cmds = RPM_DICT["x"]
        # motors.set_rpm(cmds[0], cmds[1])
        # print(motors.get_wheels_travelled())
        # diff = 0.011435 m

        while True:
            # get keyboard input
            key = input("Enter Key:").lower()
            # key = 0

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
            l_tick, r_tick = motors.get_wheels_tick()
            dl, dr = motors.get_wheels_travelled()

            print("Period: {:.4f} rpmL: {:.1f} | rpmR: {:.1f}".format(period, rpmL, rpmR))
            
            print(f"l_tick: {l_tick}, r_tick: {r_tick}")
            print(f"abs l_tick: {l_tick-L_TICK} abs r_tick: {r_tick-R_TICK}")
            print(f"rel l_tick: {l_tick-old_l_tick} rel r_tick: {r_tick-old_r_tick}")
            
            print(f"dl: {dl}, dr: {dr}")

            old_l_tick, old_r_tick = l_tick, r_tick

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