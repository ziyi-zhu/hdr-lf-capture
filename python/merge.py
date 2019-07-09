import cv2, numpy as np
import exifread, rawpy
import os, re, sys
from fractions import Fraction

class CameraParams:
	def __init__(self, k, std_read, std_adc):
		self.k = k
		self.std_read = std_read
		self.std_adc = std_adc

		self.empty = not np.any(k + [std_read, std_adc])

Camera = {
	"SonyA7r1": CameraParams( k=[2.23647, 1.32064, 5.77612], std_read = 3.19798, std_adc = 6.60121),
	"CanonT1": CameraParams( k=[4.33639, 2.56427, 9.48193], std_read = 0.0231253, std_adc = 52.4672),
	"SonyA7r3": CameraParams( k=[2.23516, 1.45227, 5.63239], std_read = 3.36703e-07, std_adc = 7.68687),
	"IDS": CameraParams( k=[13.6752, 9.88293, 8.90192], std_read = 0.570401, std_adc = 1.3521),
	"Empty": CameraParams( k=[0.,0.,0.], std_read = 0., std_adc = 0.)
}

"""
Reconstruct HDR images from multiple LDR images
filenames - list of filenames with extensions of raw images
cam - camera noise parameters
output_filename - output HDR filename with extension
"""
def merge(filenames, cam, output_filename):
	# Read raw images wihtout gamma
	images = np.array([cv2.cvtColor(rawpy.imread(f)
			 .postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16, use_camera_wb=True), cv2.COLOR_RGB2BGR)
			 for f in filenames])

	# Obtain gain and exposures used for the different captures
	exposures = np.zeros(len(filenames))
	gain = np.zeros(len(filenames))
	for i, f in enumerate(filenames):
		with open(f, 'rb') as f:
			tags = exifread.process_file(f)
			exposures[i] = float(Fraction(tags['EXIF ExposureTime'].printable))
			gain[i] = int(tags['EXIF ISOSpeedRatings'].printable) / 100

	alpha = np.zeros((images.shape))
	beta = np.zeros((images.shape))
	if cam.empty:
		alpha = 1
	else:
		for i, g in enumerate(gain):
			alpha[i] = g*np.array(list(reversed(cam.k)))
			beta[i] = cam.std_read**2 * g**2 + cam.std_adc**2

	var = images*alpha + beta
	var[var == 0] = 1	# To prevent division by 0
	del alpha			# Memory limitations
	del beta
	weights = exposures[:, np.newaxis, np.newaxis, np.newaxis]**2 / var
	saturated = np.any(images == 2**16-1, axis=3)

	# Divide by 0 is handled later
	with np.errstate(divide='ignore', invalid='ignore'):
		# HDR = np.ma.average(images / exposures[:,np.newaxis, np.newaxis, np.newaxis], weights=weights * (~saturated[:,:,:,np.newaxis]), axis=0)
		HDR = np.sum(images / exposures[:,np.newaxis, np.newaxis, np.newaxis] * (weights * (~saturated[:,:,:,np.newaxis])), axis=0) / np.sum(weights * ~saturated[:,:,:,np.newaxis], axis=0)

	# Normalise and handle nan values
	HDR = HDR / np.nanmax(HDR)
	for c in range(2):
		HDR[np.isnan(HDR[:,:,c])] = np.nanmax(HDR[:,:,c])

	cv2.imwrite(output_filename, HDR.astype(np.float32), [cv2.IMWRITE_EXR_TYPE, cv2.IMWRITE_EXR_TYPE_HALF])

"""
Merge HDR light field images
data - directory containing all the images
cam_name - name of camera used, to use noise parameters
num_exposures - number of different exposures used for a single HDR image
"""
def merge_light_field(data, cam_name, num_exposures):
	try:
		cam = Camera[cam_name]
	except KeyError as e:
		print('Camera not found, performing merge without noise model')
		cam = Camera['Empty']

	output_dir = os.path.join(data, "merged")
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	all_files = os.listdir(f'{data}/')
	for i in range(len(all_files) // num_exposures):
		files = [os.path.join(data, "{:03d}-{}.arw".format(i, f)) for f in range(num_exposures)]
		output_filename = os.path.join(output_dir, "{:03d}.exr".format(i))
		merge(files, cam, output_filename)
