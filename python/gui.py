from tkinter import filedialog, messagebox
from tkinter import *

import serial
import os
import subprocess

import gphoto2 as gp

from control import *
# from merge import merge_light_field

camera_name = 'SonyA7r1'
# hdr_merging = False

class CameraControlGUI:
    def __init__(self, master, port, baud_rate):
        self.master = master
        master.title("Camera Control")

        self.ser = serial.Serial(port, baud_rate)
        self.camera = gp.check_result(gp.gp_camera_new())       
        
        # GUI for control of motor speed
        """
        self.speed_label = Label(master, text="Current speed:")
        self.current_speed = Label(master, text="5", width=4)

        self.speed_label.grid(column=0, row=0)
        self.current_speed.grid(column=1, row=0)

        self.speed_down_button = Button(
                master, command=self.decrease_speed, text="−", height=3, width=10)
        self.speed_up_button = Button(
                master, command=self.increase_speed, text="+", height=3, width=10)
        self.speed_set_button = Button(
                master, command=self.send_speed, text="Set", height=3, width=10)

        self.speed_down_button.grid(column=2, row=0, sticky="ewns")
        self.speed_up_button.grid(column=3, row=0, sticky="ewns")
        self.speed_set_button.grid(column=4, row=0, sticky="ewns")

        """

        # GUI for adjustment of camera location
        self.location_label = Label(master, text="Current location:")
        self.current_location = Label(master, text="0", width=4)

        self.location_label.grid(column=0, row=1)
        self.current_location.grid(column=1, row=1)

        self.location_left_button = Button(master, text="<", height=3, width=10)
        self.location_right_button = Button(master, text=">", height=3, width=10)
        self.reset_button = Button(
                master, command=self.reset_location, text="Reset", height=3, width=10)

        self.location_left_button.bind("<ButtonPress>", self.move_backward)
        self.location_right_button.bind("<ButtonPress>", self.move_forward)

        self.location_left_button.bind("<ButtonRelease>", self.stop)
        self.location_right_button.bind("<ButtonRelease>", self.stop)

        self.location_left_button.grid(column=2, row=1, sticky="ewns")
        self.location_right_button.grid(column=3, row=1, sticky="ewns")
        self.reset_button.grid(column=4, row=1, sticky="ewns")

        # GUI for moving of camera to designated location
        """
        self.destination_label = Label(master, text="Move to location:")
        self.current_destination = Label(master, text="0")

        self.destination_label.grid(column=0, row=2)
        self.current_destination.grid(column=1, row=2)
        
        self.destination_left_button = Button(
                master, command=self.decrease_destination, text="<", height=3, width=10)
        self.destination_right_button = Button(
                master, command=self.increase_destination, text=">", height=3, width=10)

        self.destination_left_button.grid(column=2, row=2, sticky="ewns")
        self.destination_right_button.grid(column=3, row=2, sticky="ewns")

        self.move_button = Button(
                master, command=self.move_to_location, text="Move", height=3, width=10)
        self.move_button.grid(column=4, row=2, sticky="ewns")

        """

        # GUI for setting light field capture parameters
        self.stop_label = Label(master, text="Exposure stops:")
        self.stop_label.grid(column=0, row=3)

        self.stops = DoubleVar()
        self.stops.set(2.0)

        self.half_stop_button = Radiobutton(
                master, text="0.5EV", variable=self.stops, value=0.5, height=3, width=10)
        self.one_stop_button = Radiobutton(
                master, text="1.0EV", variable=self.stops, value=1.0, height=3, width=10)
        self.two_stop_button = Radiobutton(
                master, text="2.0EV", variable=self.stops, value=2.0, height=3, width=10)

        self.half_stop_button.grid(column=2, row=3, sticky="ewns")
        self.one_stop_button.grid(column=3, row=3, sticky="ewns")
        self.two_stop_button.grid(column=4, row=3, sticky="ewns")

        self.exposure_label = Label(master, text="Capture exposures:")
        self.exposure_label.grid(column=0, row=4)

        self.exposures = IntVar()
        self.exposures.set(3)

        self.single_exposure_button = Radiobutton(
                master, text="Single Image", variable=self.exposures, command=self.change_exposure, value=1, height=3, width=10)
        self.three_exposure_button = Radiobutton(
                master, text="3 Image", variable=self.exposures, command=self.change_exposure, value=3, height=3, width=10)
        self.five_exposure_button = Radiobutton(
                master, text="5 Image", variable=self.exposures, command=self.change_exposure, value=5, height=3, width=10)

        self.single_exposure_button.grid(column=2, row=4, sticky="ewns")
        self.three_exposure_button.grid(column=3, row=4, sticky="ewns")
        self.five_exposure_button.grid(column=4, row=4, sticky="ewns")

        self.view_label = Label(master, text="Capture views:")
        self.current_view = Label(master, text="5", width=4)

        self.view_label.grid(column=0, row=5)
        self.current_view.grid(column=1, row=5)

        self.views = IntVar()
        self.views.set(5)
        
        self.view_left_button = Button(
                master, command=self.decrease_view, text="<", height=3, width=10)
        self.view_right_button = Button(
                master, command=self.increase_view, text=">", height=3, width=10)

        self.view_left_button.grid(column=2, row=5, sticky="ewns")
        self.view_right_button.grid(column=3, row=5, sticky="ewns")

        self.view_set_button = Button(
                master, command=self.reset_view, text="Reset", height=3, width=10)
        self.view_set_button.grid(column=4, row=5, sticky="ewns")


        # GUI for camera control
        self.status_label = Label(master, text="Stopped")
        self.status_label.grid(column=0, row=6)

        self.capture_image_button = Button(
                master, command=self.capture_image, text="Capture", height=3, width=10)
        self.capture_image_button.grid(column=2, row=6, sticky="ewns")

        self.capture_light_field_button = Button(
                master, command=self.capture_light_field, text="Capture LF", height=3, width=10)
        self.capture_light_field_button.grid(column=3, row=6, sticky="ewns")

        self.exit_button = Button(
                master, command=master.destroy, text="Exit", height=3, width=10)
        self.exit_button.grid(column=4, row=6, sticky="ewns")

    def increase_speed(self):
        new_speed = int(self.current_speed.cget("text")) + 1
        self.current_speed.configure(text=str(new_speed))

    def decrease_speed(self):
        new_speed = int(self.current_speed.cget("text")) - 1
        self.current_speed.configure(text=str(new_speed))

    def send_speed(self):
        self.ser.write(b'x' + self.current_speed.cget("text").encode('UTF-8'))

    def move_forward(self, event):
        self.status_label.configure(text="Moving forward")
        self.ser.write(b'1')

    def move_backward(self, event):
        self.status_label.configure(text="Moving backward")
        self.ser.write(b'2')

    def stop(self, event):
        self.status_label.configure(text="Stopped")
        self.ser.write(b'0')
        new_location = int(self.ser.readline())
        self.current_location.configure(text=str(new_location))

    def reset_location(self):
        self.ser.write(b'r')
        self.current_speed.configure(text="5")
        self.current_location.configure(text="0")
        
    def increase_destination(self):
        new_destination = int(self.current_destination.cget("text")) + 1
        self.current_destination.configure(text=str(new_destination))

    def decrease_destination(self):
        new_destination = int(self.current_destination.cget("text")) - 1
        self.current_destination.configure(text=str(new_destination))

    def move_to_location(self):
        self.ser.write(b'm' + self.current_destination.cget("text").encode('UTF-8'))
        process = self.ser.readline()
        self.current_location.configure(text=self.current_destination.cget("text"))

    def increase_view(self):
        new_view = int(self.current_view.cget("text")) + 1
        self.current_view.configure(text=str(new_view))
        self.views.set(new_view)

    def decrease_view(self):
        new_view = int(self.current_view.cget("text")) - 1
        self.current_view.configure(text=str(new_view))
        self.views.set(new_view)

    def reset_view(self):
        self.current_view.configure(text="5")
        self.views.set(5)

    def change_exposure(self):
        if self.exposures.get() is 1:
            self.half_stop_button.configure(state = DISABLED)
            self.one_stop_button.configure(state = DISABLED)
            self.two_stop_button.configure(state = DISABLED)
        else:
            self.half_stop_button.configure(state = NORMAL)
            self.one_stop_button.configure(state = NORMAL)
            self.two_stop_button.configure(state = NORMAL)

    def show_info(self):
        if self.exposures.get() is 1:
            drive_mode = "Single Shooting"
        else:
            drive_mode = "Cont. Bracket: " + "{:.1f}EV {} Image".format(
                    self.stops.get(), self.exposures.get())
        lines = ['Drive Mode - ' + drive_mode, 'Focus Mode - Manual Focus', 'AF w/ shutter - Off', 'AEL w/ shutter - Off']
        messagebox.showinfo('Change Camera Settings', "\n".join(lines))

    def capture_image(self):
        camera_capture_image(self.camera)
        self.status_label.configure(text="Finished")

    def capture_light_field(self):
        capture_path = filedialog.askdirectory()
        self.show_info()
        camera_capture_light_field(self.camera, self.ser, self.views.get(), self.exposures.get(), 
                self.stops.get(), capture_path)
        # if hdr_merging is True:
        #     merge_light_field(capture_path, camera_name, self.exposures.get())
        self.current_location.configure(text="0")
        process = self.ser.readline()
        self.status_label.configure(text="Finished")