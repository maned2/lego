lego mindstorms - A construction kit in which you can write in Python and connect it to your computer.
main.py - main program
convert.py - audio file converter
cp.py - program for downloading sound files to the mindstorms device


sudo su
./cp.py sounds/device/battery_full my_sounds

vol 0.0625 - from instruction
vol 0.1025 - normal
vol 0.1325 - not so bad 
vol 0.1425 - bad
vol 0.1525 - bad
vol 0.2025 - bad

sox sounds/wav/calibrate_motors.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/calibrate_motors_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/calibrate_start.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/calibrate_start_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/calibrate_weapon.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/calibrate_weapon_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/calibrate_weapon_fail.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/calibrate_weapon_fail_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/dead_end.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/dead_end_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/ok.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/ok_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/pick_up.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/pick_up_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/song.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/song_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/wall.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/wall_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/women.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/women_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05
sox sounds/wav/women_v2.wav --bits 16 --channels 1 --encoding signed-integer --endian little --rate 16000 sounds/device/women_v2_1.raw vol 0.13 dcshift 0.0625 fade h 0.05 -0.05

rshell
cd /pyboard/my_sounds
ls


python3 convert_sound.py sounds/wav/start_0.wav