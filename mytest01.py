from pymba import *
import numpy as np
import cv2
import time

#very crude example, assumes your camera is PixelMode = BAYERRG8
count = 0

def frameDoneCallBack(frame):
#        imgData = frame.getBufferByteData()
        global count
        moreUsefulImgData = np.ndarray(buffer = frame.getBufferByteData(),
                                       dtype = np.uint8,
                                       shape = (frame.height,
                                                frame.width,
                                                1))
        rgb = cv2.cvtColor(moreUsefulImgData, cv2.COLOR_BAYER_RG2RGB)
        cv2.imwrite('foo{}.png'.format(count), rgb)
#        print "image {} saved".format(count)
        
        
        count += 1

        print count       
        frame.queueFrameCapture(frameDoneCallBack)


# start Vimba
with Vimba() as vimba:
    # get system object
    system = vimba.getSystem()

    # list available cameras (after enabling discovery for GigE cameras)
    if system.GeVTLIsPresent:
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)
    cameraIds = vimba.getCameraIds()
    for cameraId in cameraIds:
        print 'Camera ID:', cameraId

    # get and open a camera
    camera0 = vimba.getCamera(cameraIds[0])
    camera0.openCamera()

    # list camera features
    cameraFeatureNames = camera0.getFeatureNames()
    for name in cameraFeatureNames:
        print 'Camera feature:', name

    # read info of a camera feature
    #featureInfo = camera0.getFeatureInfo('AcquisitionMode')
    #for field in featInfo.getFieldNames():
    #    print field, '--', getattr(featInfo, field)

    # get the value of a feature
    print camera0.AcquisitionMode

    # set the value of a feature
#    camera0.AcquisitionMode = 'SingleFrame'
    camera0.AcquisitionMode = 'Continuous'

    # create new frames for the camera
    frame0 = camera0.getFrame()    # creates a frame
    frame1 = camera0.getFrame()    # creates a second frame

    # announce frames
    frame0.announceFrame()
    frame1.announceFrame()
    # Capture Engine Start    
    camera0.startCapture()
   
    frame0.queueFrameCapture(frameDoneCallBack)
    frame1.queueFrameCapture(frameDoneCallBack)
    
    # Acquisition Start
    camera0.runFeatureCommand('AcquisitionStart')
    
    # capture a camera image
    while (count<10):
        pass
        
    # Acquisition Stop
    camera0.runFeatureCommand('AcquisitionStop')
    # Capture Engine End     
    camera0.endCapture() 
    camera0.flushCaptureQueue()
    # clean up after capture
    camera0.revokeAllFrames()

    # close camera
    camera0.closeCamera()

