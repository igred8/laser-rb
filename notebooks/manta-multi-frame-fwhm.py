from vimba import *
import sys
sys.path.append('D:/Dropbox/py_projects/vimba-api/src/')
import vimbaapilib as val
from time import sleep, time_ns


def main():

    val.print_preamble()
    # change this ID if it does not match the desired camera
    # cam_id = parse_args()
    CAM_ID = 'DEV_000F314EED0D'

    NFRAMES = 11 
    FRAME_GRAB_SLEEPTIME = 0.5 # this is the sleep time between code loops. DOES NOT control the frame rate of the camera. 
    FRAME_ROI = [0,1215,250,1250] # ROI for frames [row_min, row_max, col_min, col_max], default is full frame i.e. [0, 1215, 0, 1935]

    # Vimba is to be used inside a with scope
    # .get_instance() inits vimba
    with Vimba.get_instance() as vimba:
        t1 = time_ns()
        for i in range(NFRAMES):
            
            try:
                # print(f'Attempting to get frame from Camera ID: {CAM_ID}')
                with val.get_camera(CAM_ID) as cam:
                    
                    # get frame
                    frame, frameTSstr, pixfmtstr = val.get_frame(cam, verbose=False)
                    # print('---')

                    # as np.ndarray
                    frame_np = frame.as_numpy_ndarray()
                    frame_np = frame_np[:,:,0] #  convert to 2D array, may be a problem for RGB cameras
                    # calc FWHM
                    shgpeakwidth = val.peak_fwhm(frame_np, prominence_min=5, invert=True, roi=FRAME_ROI)
                    try:
                        shgfwhmpix = shgpeakwidth[0][0][0]
                        print(f'SHG FWHM = {shgfwhmpix:0.1f} pixels')
                    except IndexError as error:
                        shgfwhmpix = 0.0
                        print('::: WARNING: Peak lost. Peak FWHM set to 0.0 pixels')
                        pass



            finally:
                # print('exit')
                sleep(FRAME_GRAB_SLEEPTIME)

            t2 = time_ns()
            print(f'elapsed time = {1e-6*(t2-t1):0.3f} ms')
            t1 = t2

if __name__ == '__main__':
    main()