from zlac8015d import ZLAC8015D

class Motors:

    # subject to change
    front_port = "/dev/ttyUSB0"
    rear_port = "/dev/ttyUSB1"

    def __init__(self):

        # initialize drivers
        front = ZLAC8015D.Controller(port=Motors.front_port)
        rear = ZLAC8015D.Controller(port=Motors.rear_port)

        front.disable_motor()
        rear.disable_motor()

        front.set_accel_time(1000,1000)
        front.set_decel_time(1000,1000)
        rear.set_accel_time(1000,1000)
        rear.set_decel_time(1000,1000)

        front.set_mode(3)
        front.enable_motor()
        rear.set_mode(3)
        rear.enable_motor()

        front_l_tick_i, front_r_tick_i = front.get_wheels_tick()
        rear_l_tick_i, rear_r_tick_i = rear.get_wheels_tick()

        self.front = front
        self.rear = rear
        self.f_tick = [front_l_tick_i,front_r_tick_i]
        self.r_tick = [rear_l_tick_i,rear_r_tick_i]

    def set_vel(self, vel_list):

        # set velocity
        self.front.set_rpm(vel_list[0],vel_list[1])
        self.rear.set_rpm(vel_list[2],vel_list[3])

    def get_tick(self):

        # compare the current tick to the original tick
        front_l_tick_i, front_r_tick_i = self.front.get_wheels_tick()
        rear_l_tick_i, rear_r_tick_i = self.rear.get_wheels_tick()

        fld = front_l_tick_i - self.f_tick[0]
        frd = front_r_tick_i - self.f_tick[1]
        rld = rear_l_tick_i - self.r_tick[0]
        rrd = rear_l_tick_i = self.r_tick[1]

        return fld, frd, rld, rrd
        
    def get_rpms(self):

        # get the rpm of teh four wheels
        flrpm, frrpm = self.front.get_rpm()
        rlrpm, rrrpm = self.rear.get_rpm()

        return (flrpm, frrpm, rlrpm, rrrpm)


    def terminate(self):

        # end the motor
        self.front.disable_motor()
        self.rear.disable_motor()
