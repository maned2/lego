from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App, MotorPair
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, \
    not_equal_to
import math, hub, random

# Create your objects here.
mshub = MSHub()

OFF = 0
PINK = 1
PURPLE = 2
BLUE = 3
TEAL = 4
GREEN = 5
LIME = 6
YELLOW = 7
ORANGE = 8
RED = 9
WHITE = 10
GREY = 11

distance_sensor = DistanceSensor('A')
dist_sensor = hub.port.A.device
color_sensor = ColorSensor('C')
left_motor = Motor('B')
right_motor = Motor('F')
motor_pair = MotorPair('B', 'F')
neck_motor = Motor('D')

sounds_dict = {
    'battery_low': {
        'time': 6,
        'file': 'battery_low1'
    },
    'battery_full': {
        'time': 6,
        'file': 'batteryfu1'
    },
    'calibrate_start': {
        'time': 4,
        'file': 'calibrate_start_1'
    },
    'calibrate_eyes': {
        'time': 4,# ?
        'file': 'calibrate_eyes1'
    },
    'calibrate_neck': {
        'time': 2,
        'file': 'calibrate_neck1'
    },
    'calibrate_motors': {
        'time': 2,
        'file': 'calibrate_motors_1'
    },
    'ok': {
        'time': 1,
        'file': 'okkkk1'
    },
    'start': {
        'time': 3,
        'file': 'sta7'
    },
    'wall': {
        'time': 5,
        'file': 'wall1'
    },
    'mom': {
        'time': 5,
        'file': 'mom1'
    },
    'song': {
        'time': 5,
        'file': 'song_1'
    }
}

ROTATING_SPEED = 10
ROTATING_DEGREES = 20
DISTANCE_HISTORY_COUNT = 2

DRIVE_LOOP_DELAY = 0.5
ROTATE_LOOP_DELAY = 0.1

STATE_DRIVE = 'drive'
STATE_ROTATING = 'rotating'

STATES_IN_LOOP = [STATE_DRIVE, STATE_ROTATING]

current_rotate_direction = -1

DISTANCE_LIMIT_STOP = 50
DISTANCE_LIMIT_BACKWARD = 20
DISTANCE_LIMIT_DRIVE = 150


distance_history = []

def loop_drive():
    global current_rotate_direction, distance_history
    current_distance = get_distance()
    if current_distance > DISTANCE_LIMIT_STOP:
        drive_forward()
        return STATE_DRIVE, DRIVE_LOOP_DELAY
    else:
        stop()
        play_sound('wall')
        check_and_drive_back(current_distance)
        current_rotate_direction = random.randint(0, 1)
        distance_history = []
        print('current_rotate_direction', current_rotate_direction)
        return STATE_ROTATING, DRIVE_LOOP_DELAY

def loop_rotate():
    global distance_history

    check_and_drive_back(get_distance())
    wait_for_seconds(0.05)
    current_distance = get_distance()
    distance_history.append(current_distance)

    if current_distance <= DISTANCE_LIMIT_DRIVE:
        rotate(current_rotate_direction)
        return STATE_ROTATING, ROTATE_LOOP_DELAY
    else:
        if check_can_drive(distance_history):
            return STATE_DRIVE, DRIVE_LOOP_DELAY
        else:
            rotate(current_rotate_direction)
            return STATE_ROTATING, ROTATE_LOOP_DELAY

STATES_FUNC = {
    STATE_DRIVE: loop_drive,
    STATE_ROTATING: loop_rotate
}

def main():
    # motion_sensor_start()
    startup()
    smile()
    # accelerometer()
    # check_battery()

    # calibrate_all()
    # drive_forward()
    # calibrate_neck()
    # drive_backward()
    # rotate()
    move_neck_middle()
    play_sound('mom')
    # play_random_sound(['mom', 'search'])
    start_main_loop()

    # rand = random.randint(0, 1)
    # print('rand', rand)


def start_main_loop():
    current_state = STATE_DRIVE
    current_delay = DRIVE_LOOP_DELAY
    while current_state in STATES_IN_LOOP:
        print('current_state', current_state)
        wait_for_seconds(current_delay)
        check_gesture()
        # current_state, current_delay = STATES_FUNC[current_state]()

def calibrate_all():
    play_sound('calibrate_start')
    wait_for_seconds(4)
    calibrate_eyes()
    calibrate_neck()
    calibrate_motors()


def calibate_light_matrix():
    mshub.light_matrix.set_pixel(1, 4, 90)


def play_sound(name, is_wait=True):
    sound = sounds_dict[name]
    hub.sound.play("my_sounds/" + sound['file'])
    if is_wait:
        # wait_for_seconds(sound['time'])
        is_open = False
        for i in range(1, sound['time'] * 4):
            if is_open:
                smile()
                is_open = False
            else:
                smile2()
                is_open = True
            wait_for_seconds(0.25)
        smile()

def play_random_sound(arr, is_wait=True):
    play_sound(arr[0], is_wait)

def smile():
    H = 9
    _ = 0

    smiley = [
        [_, H, _, H, _],
        [_, _, _, _, _],
        [_, _, _, _, _],
        [H, H, H, H, H],
        [_, _, _, _, _],
    ]

    def matrix_to_image(matrix):
        # Convert an n x m matrix to a hub Image with semicolons
        # E.g.'09090:09090:00000:90009:09990'
        # With nested list comprehensions. Why? Because I can. :P
        return hub.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

    smiley_img = matrix_to_image(smiley)
    hub.display.show(smiley_img)


def smile2():
    H = 9
    _ = 0

    smiley = [
        [_, H, _, H, _],
        [_, _, _, _, _],
        [_, H, H, H, _],
        [H, _, _, _, H],
        [_, H, H, H, _],
    ]

    def matrix_to_image(matrix):
        # Convert an n x m matrix to a hub Image with semicolons
        # E.g.'09090:09090:00000:90009:09990'
        # With nested list comprehensions. Why? Because I can. :P
        return hub.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

    smiley_img = matrix_to_image(smiley)
    hub.display.show(smiley_img)


def check_battery():
    bat_percent = hub.battery.capacity_left()
    if bat_percent >= 80:
        play_sound('battery_full')
    else:
        play_sound('battery_low')


def calibrate_eyes():
    # hub.sound.play("my_sounds/calibrate_eyes1")
    play_sound('calibrate_eyes', False)
    top_left = 0
    top_right = 0
    bottom_left = 9
    bottom_right = 9
    dist_sensor.mode(5, bytes([9, 0, 0, 0]))
    wait_for_seconds(1)
    dist_sensor.mode(5, bytes([0, 9, 0, 0]))
    wait_for_seconds(1)
    dist_sensor.mode(5, bytes([0, 0, 9, 0]))
    wait_for_seconds(1)
    dist_sensor.mode(5, bytes([0, 0, 0, 9]))
    wait_for_seconds(1)
    dist_sensor.mode(5, bytes([9, 9, 9, 9]))
    wait_for_seconds(1)
    dist_sensor.mode(5, bytes([top_left, top_right, bottom_left, bottom_right]))
    wait_for_seconds(1)
    play_sound('ok')

def move_neck_middle():
    neck_motor.run_to_position(350, 'shortest path', 20)

def calibrate_neck():
    play_sound('calibrate_neck', False)
    neck_motor.run_to_position(0, 'shortest path', 20)
    wait_for_seconds(1)
    neck_motor.run_to_position(90, 'clockwise', 20)
    wait_for_seconds(1)
    neck_motor.run_to_position(270, 'counterclockwise', 20)
    wait_for_seconds(1)
    play_sound('ok')

def check_can_drive(array):
    is_can_drive = False
    count_can_drive = 0
    for i in array:
        if i > DISTANCE_LIMIT_DRIVE:
            count_can_drive = count_can_drive + 1
        else:
            count_can_drive = 0

        if count_can_drive > DISTANCE_HISTORY_COUNT:
            is_can_drive = True
            break

    return is_can_drive


def calibrate_motors():
    play_sound('calibrate_motors', False)
    motor_pair.move(20, 'cm', 0)
    wait_for_seconds(1)
    play_sound('ok')


def startup():
    hub.led(GREEN)
    mshub.light_matrix.rotate('counterclockwise')
    hub.sound.volume(10)
    mshub.speaker.set_volume(100)
    play_sound('start')

def rotate(direction):
    if direction == 0:
        motor_pair.start(100, ROTATING_SPEED)
        # motor_pair.move(ROTATING_DEGREES, 'degrees', -100, ROTATING_SPEED)
    elif direction == 1:
        motor_pair.start(-100, ROTATING_SPEED)
        # motor_pair.move(ROTATING_DEGREES, 'degrees', 100, ROTATING_SPEED)

def drive_forward():
    # motor_pair.move(-100, 'cm', 0, -100)
    # motor_pair.move_tank(100, 'cm', 100, 100)
    motor_pair.start(0, 100)

def drive_backward():
    motor_pair.move_tank(-100, 'cm', 100, 100)

def check_and_drive_back(distance):
    if distance <= DISTANCE_LIMIT_BACKWARD:
        drive_backward_cm(10)

def drive_backward_cm(cm):
    motor_pair.move_tank(cm * -1, 'cm', 100, 100)

def stop():
    motor_pair.stop()

def motion_sensor_start():
    # define method
    def motion_callback(gesture):
        print(gesture)
    # attach it as callback.
    # hub.motion.gesture(motion_callback)

def buttons_start():
    hub.button.left.callback(lambda time_ms: print('left button pressed', time_ms))
    hub.button.center.callback(lambda time_ms: print('center button pressed', time_ms))
    hub.button.right.callback(lambda time_ms: print('right button pressed', time_ms))

def accelerometer():
    left_right, down_up, front_back = hub.motion.accelerometer_filter()
    print('accelerometer', left_right, down_up, front_back)

def get_distance():
    distance = distance_sensor.get_distance_cm()
    print('distance', distance)
    if distance is not None:
        return distance
    else:
        return 200

def check_gesture():
    if mshub.motion_sensor.was_gesture('doubletapped'):
        play_sound('song')


main()