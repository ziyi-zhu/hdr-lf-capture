from tkinter import Tk, Label, Button, Entry

import serial
import os
import subprocess

import gphoto2 as gp

from control import *
# from merge import merge_light_field

# parameters for hdr light field capture
N_VIEWS = 11
N_EXPOSURES = 3

camera_name = 'SonyA7r1'
capture_path = '/home/pi/Pictures/capture'
# hdr_merging = False

class CameraControlGUI:
    def __init__(self, master, port, baud_rate):
        self.master = master
        master.title("Camera Control")

        self.ser = serial.Serial(port, baud_rate)
        self.camera = gp.check_result(gp.gp_camera_new())
        
        self.speed_label = Label(master, text="Current speed:")
        self.current_speed = Label(master, text="5", width=5)

        self.speed_label.grid(column=0, row=0)
        self.current_speed.grid(column=1, row=0)

        self.speed_down_button = Button(
                master, command=self.decrease_speed, text="−", height=3, width=10)
        self.speed_up_button = Button(
                master, command=self.increase_speed, text="+", width=10)
        self.speed_set_button = Button(
                master, command=self.send_speed, text="Set", width=10)

        self.speed_down_button.grid(column=2, row=0, sticky="ewns")
        self.speed_up_button.grid(column=3, row=0, sticky="ewns")
        self.speed_set_button.grid(column=4, row=0, sticky="ewns")

        self.location_label = Label(master, text="Current location:")
        self.current_location = Label(master, text="0")

        self.location_label.grid(column=0, row=1)
        self.current_location.grid(column=1, row=1)

        self.location_left_button = Button(master, text="<", height=3)
        self.location_right_button = Button(master, text=">")
        self.reset_button = Button(
                master, command=self.reset_location, text="Reset")

        self.location_left_button.bind("<ButtonPress>", self.move_backward)
        self.location_right_button.bind("<ButtonPress>", self.move_forward)

        self.location_left_button.bind("<ButtonRelease>", self.stop)
        self.location_right_button.bind("<ButtonRelease>", self.stop)

        self.location_left_button.grid(column=2, row=1, sticky="ewns")
        self.location_right_button.grid(column=3, row=1, sticky="ewns")
        self.reset_button.grid(column=4, row=1, sticky="ewns")

        self.destination_label = Label(master, text="Move to location:")
        self.current_destination = Label(master, text="0")

        self.destination_label.grid(column=0, row=2)
        self.current_destination.grid(column=1, row=2)
        
        self.destination_left_button = Button(
                master, command=self.decrease_destination, text="<", height=3)
        self.destination_right_button = Button(
                master, command=self.increase_destination, text=">")

        self.destination_left_button.grid(column=2, row=2, sticky="ewns")
        self.destination_right_button.grid(column=3, row=2, sticky="ewns")

        self.move_button = Button(
                master, command=self.move_to_location, text="Move")
        self.move_button.grid(column=4, row=2, sticky="ewns")

        self.status_label = Label(master, text="Stopped")
        self.status_label.grid(column=0, row=3)

        self.capture_image_button = Button(
                master, command=self.capture_image, text="Capture", height=3)
        self.capture_image_button.grid(column=2, row=3, sticky="ewns")

        self.capture_light_field_button = Button(
                master, command=self.capture_light_field, text="Capture LF")
        self.capture_light_field_button.grid(column=3, row=3, sticky="ewns")

        self.exit_button = Button(
                master, command=master.destroy, text="Exit")
        self.exit_button.grid(column=4, row=3, sticky="ewns")

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

    def capture_image(self):
        camera_capture_image(self.camera)
        self.status_label.configure(text="Finished")

    def capture_light_field(self):
        camera_capture_light_field(self.camera, self.ser, N_VIEWS, N_EXPOSURES, capture_path)
        # if hdr_merging is True:
        #     merge_light_field(capture_path, camera_name, N_EXPOSURES)
        self.current_location.configure(text="0")
        self.status_label.configure(text="Finished")