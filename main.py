from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, \
    not_equal_to
# import math
from mindstorms import Motor, App
import hub
# import runtime
# import sys
# import system
import time
import os

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

mshub = MSHub()

rudder_motor = Motor('A')
drive_motor = Motor('B')
sensor_motor = Motor('C')
distance_sensor = DistanceSensor('E')
dist_sensor = hub.port.E.device


def get_distance():
    # Get a distance reading in cm
    wait_for_seconds(0.05)
    # distance = dist_sensor.get()[0]
    distance = distance_sensor.get_distance_cm()
    if distance is not None:
        return distance
    else:
        return 200


def display(val):
    hub.display.show(str(val))


def drive():
    while get_distance() > 50:
        drive_motor.start(-100)

    stop()
    get_new_direction()
    # if get_distance() > 50:
    #    drive_motor.start(-100)
    #    drive()
    # else:
    #    stop()
    #    get_new_direction()

    # wait_for_seconds(0.5)
    # if get_distance() > 50:
    #    # play_sound
    #    # hub.sound.play("sounds/dont_disturb")
    #    drive()
    # else:
    #    stop()
    #    get_new_direction()


def stop():
    mshub.speaker.beep()
    drive_motor.stop()


def eyes_all():
    top_left = 9
    top_right = 9
    bottom_left = 9
    bottom_right = 9
    dist_sensor.mode(5, bytes([top_left, top_right, bottom_left, bottom_right]))


def eyes_bottom():
    top_left = 0
    top_right = 0
    bottom_left = 9
    bottom_right = 9
    dist_sensor.mode(5, bytes([top_left, top_right, bottom_left, bottom_right]))


def calibrate_rudder():
    rudder_motor.run_to_position(60, 'shortest path', 20)
    wait_for_seconds(1)
    rudder_motor.run_to_position(0, 'shortest path', 20)
    print('rudder', rudder_motor.get_position())
    wait_for_seconds(1)
    rudder_motor.run_to_position(300, 'shortest path', 20)
    wait_for_seconds(1)
    rudder_motor.run_to_position(0, 'shortest path', 20)
    print('rudder', rudder_motor.get_position())


def calibrate():
    hub.sound.play("my_sounds/calibratestart")
    wait_for_seconds(35)
    hub.led(YELLOW)
    eyes_bottom()
    sensor_motor.run_to_position(180, 'shortest path', 10)
    calibrate_rudder()
    hub.led(GREEN)


def smile():
    H = 9
    _ = 0

    smiley = [
        [_, H, _, H, _],
        [_, H, _, H, _],
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


def move_angle(angle):
    print(angle)
    hub.sound.play("my_sounds/song_")
    wait_for_seconds(4)
    # if direction == 'left':
    #    rudder_motor.run_to_position(-90, 'shortest path', 100)
    # elif direction == 'right':
    #    rudder_motor.run_to_position(90, 'shortest path', 100)
    #
    # drive_motor.run_for_seconds(5, -100)
    # rudder_motor.run_to_position(0, 'shortest path', 100)
    # drive()


def get_sensor_angle():
    angle = 180 - sensor_motor.get_position()
    angle = angle - angle * 2
    return angle


def get_new_direction():
    hub.sound.play("my_sounds/wall__")
    wait_for_seconds(4)
    hub.sound.play("my_sounds/search")
    wait_for_seconds(3)
    is_found = False
    position = sensor_motor.get_position()
    while get_distance() < 150 and position > 90:
        print('sensor_motor_position', position)
        sensor_motor.run_to_position(position - 10, 'shortest path', 10)
        wait_for_seconds(0.5)
        position = sensor_motor.get_position()

    distance = get_distance()
    if distance >= 150:
        print('distance', distance)
        angle = get_sensor_angle()
        print('angle', angle)
        sensor_motor.run_to_position(180, 'shortest path', 10)
        move_angle(angle)
    else:
        sensor_motor.run_to_position(180, 'shortest path', 10)
        while get_distance() < 150 and sensor_motor.get_position() < 270:
            sensor_motor.run_to_position(sensor_motor.get_position() + 10, 'shortest path', 10)
            print('sensor_motor_position', position)

        distance = get_distance()
        if distance >= 150:
            print('distance', distance)
            angle = get_sensor_angle()
            print('angle', angle)
            sensor_motor.run_to_position(180, 'shortest path', 10)
            move_angle(angle)


def check_battery():
    bat_percent = hub.battery.capacity_left()
    if bat_percent >= 80:
        hub.sound.play("my_sounds/batteryful")
        wait_for_seconds(5)
    else:
        hub.sound.play("my_sounds/batterylow")
        wait_for_seconds(5)


def main():
    eyes_all()
    print('battery', hub.battery.capacity_left())
    hub.led(GREEN)
    print('print(hub.sound.volume())', hub.sound.volume())
    hub.sound.volume(100)
    print('print(hub.sound.volume())', hub.sound.volume())
    mshub.speaker.set_volume(100)
    hub.sound.play("my_sounds/start_")
    wait_for_seconds(2)

    check_battery()
    calibrate()
    drive()

    # hub.display.start_animation('Play')
    # smile()
    # hub.light_matrix.show_image('HAPPY')
    # wait_for_seconds(5)
    # hub.light_matrix.off()
    # motor = Motor('C')
    # hub.display.show(str(motor.get_position()))
    # hub.light_matrix.off()
    # motor.position()


# def check():


# Write your program here.
# mshub.speaker.beep()

# # Импорт класса Motor.
# # Инициализация мотора, подключенного к порту A.

# Вращение мотора на 360° по часовой стрелке.
# motor.run_to_position(110, 'shortest path', 10)
# app.play_sound('Applause 1')
# hub.light_matrix.show_image('HAPPY')
# hub.light_matrix.show_image('GO_RIGHT')

main()