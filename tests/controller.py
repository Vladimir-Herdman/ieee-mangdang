"""Goal: Use pygame-ce for controller input, and pykey to send related
         hardware level keypresses.

Description:
    Overall, the idea here's to use pygame to get controller input from
    a bluetooth connection, and use the controller inputs to then map to
    keyboard presses the computer would need to send to the dogbot for
    actual movement to occur.

Setup:
    - Connect to dogbot via ssh.
    - Have three terminals open via tmux (or somehow).
        - In one terminal, run `ros2 launch mini_pupper_bringup bringup.launch.py`
        - In the other terminal, run `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
        - Run this python file in the third terminal

Links:
    - pygame-ce github: https://github.com/pygame-community/pygame-ce
    - pyKey github: https://github.com/gauthsvenkat/pyKey
"""
