"""Make MiniPupper move using pygame and a controller.

Setup:
    1. ssh into minipupper.
    2. run `bluetoothctl`, then from within run...
        a) `power on`
        b) `agent on`
        c) `scan on` (put controller in pairing mode before scan on)
    3. From here, you'll need the MAC address of the controller (pretend
        `A1:B2:C3:D4:E5:F6`). When `scan on` ran, 'Wireless Controller'
        should show up as an option, so you don't need the MAC address
        before all this is ran.
        a) `pair A1:B2:C3:D4:E5:F6`
        b) `trust A1:B2:C3:D4:E5:F6`
        c) `connect A1:B2:C3:D4:E5:F6`
        d) `scan off`
        e) `exit`
    4. Run the terminal command and python file (I use tmux for two terminals)
        a) `ros2 launch mini_pupper_bringup bringup.launch.py`
        b) `python3 controller_node.py`
"""
#Most of this comes from the minipupper documentation, playing around
#and reading minipupper code, and the controller test file in /tests/
from geometry_msgs.msg import Twist
from MangDang.mini_pupper.display import Display, BehaviorState
import pygame
import rclpy
from rclpy.node import Node

rclpy.init()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("<path to rocky music once sent over ssh>")
joystick = pygame.joystick.Joystick(0)

class ControllerNode(Node):
    def __init__(self):
        super().__init__("controller_teleop")
        self.disp = Display()
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.loop)

        self.max_linear_speed = 0.3
        self.max_angular_speed = 1.0
        self.deadzone = 0.3
        
        self.music_started = False

    def apply_deadzone(self, value):
        return value if abs(value) > self.deadzone else 0.0

    def loop(self):
        pygame.event.pump()
        twist = Twist()

        yaxis = -self.apply_deadzone(self.joystick.get_axis(1))
        xaxis = -self.apply_deadzone(self.joystick.get_axis(0))
        twist.linear.x = yaxis * self.max_linear_speed
        twist.angular.z = xaxis * self.max_angular_speed

        bottombutton = joystick.get_button(0)
        rightbutton  = joystick.get_button(1)
        leftbutton   = joystick.get_button(2)
        topbutton    = joystick.get_button(3)
        if bottombutton == 1:
            self.disp.show_image('<insert path to angry once pngs sent through ssh>')
        elif rightbutton == 1:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        elif leftbutton == 1:
            self.disp.show_image('<insert path to struggle once pngs sent through ssh>')
        elif topbutton == 1 and not self.music_started:
            pygame.mixer.music.play()
            self.music_started = True

        self.publisher.publish(twist)

node = ControllerNode()

try:
    rclpy.spin(node)
except (KeyboardInterrupt, SystemExit):
    pass
finally:
    node.publisher.publish(Twist())
    node.destroy_node()
    rclpy.shutdown()
    pygame.quit()
    pygame.mixer.music.unload()

# while running:
#     xaxis = joystick.get_axis(0)
#     yaxis = joystick.get_axis(1)
#     if yaxis <= -.3:
#         pass
#         # player_pos.y -= 300 * dt
#     if yaxis >= .3:
#         pass
#         # player_pos.y += 300 * dt
#     if xaxis <= -.3:
#         pass
#         # player_pos.x -= 300 * dt
#     if xaxis >= .3:
#         pass
#         # player_pos.x += 300 * dt
#
#     #0 - bottom, 1 - right, 2 - left, 3 - top
#     bottombutton = joystick.get_button(0)
#     rightbutton  = joystick.get_button(1)
#     leftbutton   = joystick.get_button(2)
#     topbutton    = joystick.get_button(3)
#     if bottombutton == 1:
#         pass
#         # circle_color = "green"
#     if rightbutton == 1:
#         pass
#         # circle_color = "orange"
#     if leftbutton == 1:
#         pass
#         # circle_color = "yellow"
#     if topbutton == 1:
#         pass
#         # circle_color = "red"
#
# pygame.quit()
