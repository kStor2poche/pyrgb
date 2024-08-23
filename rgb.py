#! /usr/bin/python
# RGB color conversion scrpit

import os;

from PIL import ImageGrab
from time import sleep
import signal
import sys


class colors:
    BLK = "\033[38;2;0;0;0m"
    GRY = "\033[38;2;128;128;128m"
    WHT = "\033[38;2;255;255;255m"
    RST = "\033[0m"


wayland = "WAYLAND_DISPLAY" in os.environ


def screencolor_picker_wayland() -> str:
    import dbus
    from gi.repository import GLib
    from dbus.mainloop.glib import DBusGMainLoop

    ret = ""

    def response_handler(response, result):
        nonlocal ret
        if response != 0:
            print("Failed to get color")
        else:
            res_color = result["color"]
            ret = str(round(res_color[0], 3))+", "\
                 +str(round(res_color[1], 3))+", "\
                 +str(round(res_color[2], 3))
        loop.quit()

    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    con_name = bus.get_connection().get_unique_name()[1:].replace(".", "_")
    response_path = f"/org/freedesktop/portal/desktop/request/{con_name}/my_token"
    bus.add_signal_receiver(
        response_handler,
        dbus_interface="org.freedesktop.portal.Request",
        path=response_path,
    )

    desktop = bus.get_object("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop")
    desktop.PickColor("PickColor", {"handle_token": "my_token"}, dbus_interface="org.freedesktop.portal.Screenshot")
    loop = GLib.MainLoop()
    loop.run()
    return ret


def screencolor_picker_x11():
    from Xlib.display import Display
    from Xlib.ext import xinput
    display = Display()
    root = display.screen().root
    root.xinput_select_events([(xinput.AllDevices,
                                xinput.ButtonPressMask)])
    # wait for mouse click
    print("Click on the spot you want to take a sample from...")
    _ = display.next_event()
    coord = root.query_pointer()._data
    x = coord["root_x"]
    y = coord["root_y"]
    display.close()
    img = ImageGrab.grab()
    return str(list(img.getpixel((x, y)))).replace('[', '').replace(']', '')


def interrupt_handler(sig, frame):
    print("\nExiting...")
    exit(0)


_ = signal.signal(signal.SIGINT, interrupt_handler)

# conversion functions
# (only 3 are needed)


def hexto8bit(h: str) -> list[int]:
    bit: list[int] = []
    for i in range(len(h)//2):
        bit.append(int(h[0+i*2:2+i*2], 16))
    return bit


def bit8tonorm(bit: list[int]) -> list[float]:
    return [round(bit[i]/255, 3) for i in range(len(bit))]


def normtohex(n: list[float]) -> str:
    h = ''
    for i in range(len(n)):
        htemp = hex(round(n[i]*255))[2:]
        h = h + ("0"+htemp)*(len(htemp) != 2) + (htemp)*(len(htemp) == 2)  # avoids an if statement
    return h


def print_color_squares(bit: list[int]):
    if len(bit) >= 3:
        print(f"\n                           \
    {colors.BLK}  🭁████🭌\
    {colors.GRY}  🭁████🭌\
    {colors.WHT}  🭁████🭌\
    {colors.RST}")
        print(f"The color looks like this :\
    {colors.BLK}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.BLK}██\
    {colors.GRY}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.GRY}██\
    {colors.WHT}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.WHT}██")
        print(f"                           \
    {colors.BLK}  🭒████🭝\
    {colors.GRY}  🭒████🭝\
    {colors.WHT}  🭒████🭝\
    {colors.RST}\n")
    if len(bit) > 3:
        print("(only the first three values were taken into account)")


def main():
    if len(sys.argv) == 1:
        inpt = input("Enter the color value that you want to convert > ")
    else:
        inpt = sys.argv[1]
        if (inpt == "-h") or (inpt == "--help"):
            print("Usage : rgb { -h | -p | (color) }\n\n\
    --help\n\
    -h      Show this help message :)\n\
    \n\
    -p      Pick color from current screen. Appending the option with a number\n\
            will add [number] seconds of delay before user is prompted to choose color.\n\
    \n\
    (color) A color among any of these three types of data : \n\
        - A hexadecimal value in the form of \"#hhhhhh\" or \"hhhhhh\"\n\
        - An array of normalized values in the form of \"d.d,d.d,d.d\"\n\
        - An array of decimal 8-bit values in the form of \"d,d,d\"\n\n\
    Note that the arrays can have a dimension different to 3")
            exit(0)
        elif (len(inpt) >= 2 and inpt[0:2] == "-p"):
            delay = "none"
            if (len(sys.argv) >= 3):
                delay = sys.argv[2]
            elif (len(inpt) > 2):
                delay = inpt[2:]
            if (delay.isdigit()):  # not working properly for double digits
                print("Waiting ", int(delay), " second", "s"*(int(delay) > 1),
                      " before accepting for user input...", sep='')
                sleep(int(delay))
            elif delay != "none":
                print("Delay\"", delay, "\"invalid.")
            if wayland:
                inpt = screencolor_picker_wayland()
            else:
                inpt = screencolor_picker_x11()

    if len(inpt) == 0:
        print("You need to provide a value. See rgb.py -h for the different forms of input accepted.", file=sys.stderr)
        exit(-1)

    if "." in inpt:
        # type = norm
        inpt = inpt.split(",")
        inpt = list(map(float, inpt))
        for i in inpt:
            if i < 0. or i > 1.:
                print("Error : input value", i, "out of range for a normalized decimal color !",  file=sys.stderr)
                exit(1)
        print("\nInput identified as normalized values", inpt)
        h = normtohex(inpt)
        bit = hexto8bit(h)
        print(f"\n• Hexadecimal :          #{h}")
        print(f"• 8-bit decimal values : {bit}".replace(']', '').replace('[', ''))
        print_color_squares(bit)
    elif "," in inpt:
        # type = 8bit
        inpt = inpt.split(",")
        inpt = list(map(int, inpt))
        for i in inpt:
            if i > 255 or i < 0:
                print("Error : input value", i, "out of range for an 8-bit decimal color !", file=sys.stderr)
                exit(1)
        print("\nInput identified as 8-bit decimal values", inpt)
        bit = inpt
        n = bit8tonorm(inpt)
        h = normtohex(n)
        print(f"\n• Normalized values : {n}".replace(']', '').replace('[', ''))
        print(f"• Hexadecimal :       #{h}")
        print_color_squares(bit)
    else:
        # type = hex
        if inpt[0] == '#':
            inpt = inpt[1:]
        for i in inpt:
            if not (i in "0123456789abcdefABCDEF"):
                print("Error : input value", i, "out of range for a hexadecimal color !", file=sys.stderr)
                exit(1)
        inpt = inpt.lower()
        print("\nInput identified as hex value #",inpt,sep='')
        bit = hexto8bit(inpt)
        n = bit8tonorm(bit)
        print(f"\n• 8-bit decimal values : {bit}".replace(']', '').replace('[', ''))
        print(f"• Normalized values :    {n}".replace(']', '').replace('[', ''))
        print_color_squares(bit)


if __name__ == "__main__":
    main()
