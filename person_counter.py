#import libs

import cv2 as cv
import numpy as np
import imutils
from collections import defaultdict
from tracker import CentroidTracker

import tensorflow as tf
import tensorflow_hub as hub

from tracker import CentroidTracker


#model load -faster_rcnn- high performance, fps:0.09-0.11  ;  mobilenet_v2- fast, fps:4.-7.
# module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" 
module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
detector = hub.load(module_handle).signatures['default']


ct = CentroidTracker()
(H, W) = (None, None)

def run_detector(detector, path):
  cap = cv.VideoCapture(path)

  #video save
  fw = int(cap.get(3))
  fh = int(cap.get(4))
  fourcc = cv.VideoWriter_fourcc(*'FMP4')
  out = cv.VideoWriter("output7.mp4", fourcc, 25.0, (fw,fh))
  # out = cv.VideoWriter('/home/elif/Documents/my_virtual_env/TFODCourse/AYVOS_Test_Case/AYVOS TEST CASE/AyvosCaseStudy/output.mp4', fourcc, 30,(393,700), True)
  # out = cv.VideoWriter('/home/elif/Documents/my_virtual_env/TFODCourse/AYVOS_Test_Case/AYVOS TEST CASE/AyvosCaseStudy/filename.avi', cv.VideoWriter_fourcc(*'MJPG'), 10, (393,700))

  counter = 0 #person counter

  #object_detect
  while True:
    ret, frame = cap.read()
    if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      break
    rect_coordinates = []
    # #more fast
    frame = imutils.resize(frame, width=700) #frame.shape = (393, 700, 3)

    #numpy nd array convert to tf eager tensore
    frame = tf.convert_to_tensor(frame, dtype=tf.uint8)

    #run_Detector_startframe
    converted_img  = tf.image.convert_image_dtype(frame, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)        


    result = {key:value.numpy() for key,value in result.items()}

    #threshold : resnet:0.45, mobilenet:0.17-0.2
    image, boxes, class_names, scores, min_score = frame.numpy(),  result["detection_boxes"], result["detection_class_entities"], result["detection_scores"], 0.3
    image_rgb = cv.cvtColor(np.uint8(image), cv.COLOR_BGR2RGB) #convert2RGB
    im_width, im_height = image_rgb.shape[:2]
    #draw boxes
    for i in np.arange(0,boxes.shape[0]):

      if class_names[i].decode("ascii") =="Person":
          
        if  scores[i] > min_score: #threshold value
          person_box =  boxes[i] * np.array([im_width, im_height, im_width, im_height])
          (y1, x1, y2, x2) = person_box.astype("int")
          box = person_box.astype("int")
          rect_coordinates.append(box.astype("int")) #[array([228, 589, 297, 626]), array([287,  75, 387, 136])]
          cv.rectangle(image_rgb, (x1, y1), (x2, y2), (0,0,255),2)   #kutu icine alma   
          
    #run_Detector_finish

    #tracking start   
    objects = ct.update(rect_coordinates) 


    for key in objects.keys():
      if int(key) > counter:
        counter = key
    person_count_text = "Person count: {}".format(counter)
    cv.putText(image_rgb, person_count_text, (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


    #video save
    out.write(image_rgb)

    #video show
    cv.imshow("outputVideo", image_rgb)
    key = cv.waitKey(1)
    if key == ord('q'):
      break

  cv.destroyAllWindows()
  cap.release()
  out.release()
  cv.destroyAllWindows()

run_detector(detector, "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/video.mov"  )
