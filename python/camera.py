from control import *

port = '/dev/ttyACM0'
baud_rate = 9600

if __name__ == '__main__':
    root = Tk()
    app = CameraControl(root, port, baud_rate)
    app.master.attributes("-fullscreen", False)
    root.mainloop()