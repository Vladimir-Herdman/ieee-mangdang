This directory is for storing all the code/project ideas used for the mangdang
school project YOU are a part of dawg.

# Personal notes on how to setup this whole thing from a Macbook
First off, open up a Docker Ubuntu Container for all this. Layers of
abstraction look good on a resume, maybe (it's the only way it worked
on my mac).
## Mini-Pupper SSH Connection
This is connecting to the Mini-Pupper through ssh on a host machine.
1. Open Ubuntu installation through USB (from boot up options)
2. Set up mobile hotspot on phone
	a) iphone name: `ONUdogbot`
	b) hotspot password: `gobears!`
3. ssh into the dogbot
	a) Make sure laptop also connected to phone hotspot
	b) terminal command: `ssh ubuntu@172.20.10.5`
	c) password once inside:  `mangdang`
### Controlling Mini-Pupper Movement with Keyboard
1. source setup script (if not done on this computer yet): `. ~/ros2_ws/install/setup.bash`
2. Run 2 commands at once, so use tmux to run both in terminal applications (within ssh)
	a) `ros2 launch mini_pupper_bringup bringup.launch.py`
	b) `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
