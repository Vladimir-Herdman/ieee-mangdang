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
        - joystick documentation: https://pyga.me/docs/ref/joystick.html#module-pygame.joystick
    - pyKey github: https://github.com/gauthsvenkat/pyKey
"""
#Most of the code here is taken and massaged verbatum from the pygame
#documentation website
import pygame

def indent(text, indentation_level=0):
    return ("    " * indentation_level) + text

def display_controller_button_info(joystick):
    jid = joystick.get_instance_id()
    lines = []
    indentation = 0

    lines.append(indent(f"Number of joysticks: {1}", indentation))
    indentation += 1

    lines.append(indent(f"Joystick {jid}", indentation))
    indentation += 1

    # Get the name from the OS for the controller/joystick.
    name = joystick.get_name()
    lines.append(indent(f"Joystick name: {name}", indentation))

    guid = joystick.get_guid()
    lines.append(indent(f"GUID: {guid}", indentation))

    power_level = joystick.get_power_level()
    lines.append(indent(f"Joystick's power level: {power_level}", indentation))

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other. Triggers count as axes.
    axes = joystick.get_numaxes()
    lines.append(indent(f"Number of axes: {axes}", indentation))
    indentation += 1

    for i in range(axes):
        axis = joystick.get_axis(i)
        lines.append(indent(f"Axis {i} value: {axis:>6.3f}", indentation))
        indentation -= 1

        buttons = joystick.get_numbuttons()
        lines.append(indent(f"Number of buttons: {buttons}", indentation))
        indentation += 1

        for i in range(buttons):
            button = joystick.get_button(i)
            lines.append(indent(f"Button {i:>2} value: {button}", indentation))
            indentation -= 1

            hats = joystick.get_numhats()
            lines.append(indent(f"Number of hats: {hats}", indentation))
            indentation += 1

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                lines.append(indent(f"Hat {i} value: {str(hat)}", indentation))
            indentation -= 2

        # draw the accumulated text
        screen.blit(
            font.render("\n".join(lines), True, "black", "white", wraplength), (10, 10)
        )

pygame.init()

font = pygame.font.SysFont(None, 25)
wraplength = 1280 - 20

#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystick = pygame.joystick.Joystick(0)

pygame.display.set_caption("Bluetooth Joystick Example")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle_color = "red"
print_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.JOYBUTTONDOWN:
        #      print(str(print_count) + ":Joystick button pressed")
        #      print_count += 1
        # if event.type == pygame.JOYAXISMOTION:
        #     #0 left-stick left/right, 1 left-stick up/down
        #      print(str(print_count) + ":Joystick axis moved")
        #      print_count += 1

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    pygame.draw.circle(screen, circle_color, player_pos, 40)

    xaxis = joystick.get_axis(0)
    yaxis = joystick.get_axis(1)
    if yaxis <= -.3:
        player_pos.y -= 300 * dt
    if yaxis >= .3:
        player_pos.y += 300 * dt
    if xaxis <= -.3:
        player_pos.x -= 300 * dt
    if xaxis >= .3:
        player_pos.x += 300 * dt

    #0 - bottom, 1 - right, 2 - left, 3 - top
    bottombutton = joystick.get_button(0)
    rightbutton  = joystick.get_button(1)
    leftbutton   = joystick.get_button(2)
    topbutton    = joystick.get_button(3)
    if bottombutton == 1:
        circle_color = "green"
    if rightbutton == 1:
        circle_color = "orange"
    if leftbutton == 1:
        circle_color = "yellow"
    if topbutton == 1:
        circle_color = "red"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    if keys[pygame.K_d]:
        display_controller_button_info(joystick)
    if keys[pygame.K_r]:
        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(30) / 1000

pygame.quit()
