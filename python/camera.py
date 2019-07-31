from gui import *

# specify the port and baud rate for serial communication
port = '/dev/ttyACM0'
baud_rate = 9600

if __name__ == '__main__':
    root = Tk()
    app = CameraControlGUI(root, port, baud_rate)
    app.master.attributes('-type', 'splash')
    root.mainloop()