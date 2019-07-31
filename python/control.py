import serial
import os
import subprocess

import gphoto2 as gp

"""
List all the files on the camera
camera - gp_camera object
path - path on the camera where photos are stored

"""
def list_files(camera, path='/'):
    result = []
    # get files
    for name, value in gp.check_result(
            gp.gp_camera_folder_list_files(camera, path)):
        result.append(os.path.join(path, name))
    # read folders
    folders = []
    for name, value in gp.check_result(
            gp.gp_camera_folder_list_folders(camera, path)):
        folders.append(name)
    # recurse over subfolders
    for name in folders:
        result.extend(list_files(camera, os.path.join(path, name)))
    return result

"""
Capture a single image and store in path
camera - gp_camera object
path - path on the Raspberry Pi where captured images are stored

"""
def camera_capture_image(camera, path='/tmp'):
    # initialize camera
    gp.check_result(gp.gp_camera_init(camera))
    # capture a image
    file_path = gp.check_result(gp.gp_camera_capture(
            camera, gp.GP_CAPTURE_IMAGE))
    # store a image
    target = os.path.join(path, file_path.name)
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    # subprocess.call(['xdg-open', target])
    # exit camera
    gp.check_result(gp.gp_camera_exit(camera))

"""
Capture light field as a set of images and store in path
camera - gp_camera object
ser - Serial object for serial communication
path - path on the Raspberry Pi where captured images are stored
n_views - number of views for the capture
n_exposures - number of exposures for the camera bracketing mode

"""
def camera_capture_light_field(camera, ser, n_views, n_exposures, stops=2.0, path='/tmp'):
    # initialize camera location
    ser.write(b'm0')
    # check and create output dirctory for capture
    output_dir = os.path.join(path, "capture")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        n_folder = 0
        while os.path.exists(output_dir):
            n_folder += 1
            output_dir = os.path.join(path, "capture-{}".format(n_folder))
        os.mkdir(output_dir)
    # capture process
    for capture_location in range(n_views):
        # initialize camera
        gp.check_result(gp.gp_camera_init(camera))
        # wait for camera to stop moving and trigger camera capture
        process = ser.readline()
        gp.check_result(gp.gp_camera_trigger_capture(camera))
        # move to the next location
        if capture_location is not n_views-1:
            ser.write(b'm' + str((capture_location+1)*(100//(n_views-1))).encode('UTF-8'))
        # save the captured files to path    
        file_number = 0
        while file_number < n_exposures:
            gp.check_result(gp.gp_camera_wait_for_event(
                    camera, gp.GP_EVENT_FILE_ADDED))
            # wait for new available file
            file_list = list_files(camera)
            # save the new file
            if len(file_list) is not file_number:
                # file format: capt-<sequence>-<distance(mm)>[<exposure(EV)>].arw
                # e.g. capt-001-0100[-2.0].arw
                target = os.path.join(output_dir, "capt-{:0>3d}-{:0>4d}[{:+.1f}]".format(
                        capture_location*n_exposures + file_number, int(capture_location*(1000/(n_views-1))),
                        stops*(file_number-n_exposures//2)) + file_list[file_number][-4:])
                camera_file = gp.check_result(gp.gp_camera_file_get(
                        camera, '/', file_list[file_number][1:], gp.GP_FILE_TYPE_NORMAL))
                gp.check_result(gp.gp_file_save(camera_file, target))
                file_number += 1
        # exit camera
        gp.check_result(gp.gp_camera_exit(camera))
    # return to initial location
    ser.write(b'm0')