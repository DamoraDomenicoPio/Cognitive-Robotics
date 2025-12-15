import numpy as np 
import cv2 
import tensorflow as tf 
from tensorflow.keras.models import load_model
import time
import os 

class EmotionExtractor():
    
    def __init__(self):
        faceProto = '/home/ddp22/Desktop/Esame/ChatBot/ROS/src/camera_pkg/src/opencv_face_detector.pbtxt'
        faceModel = '/home/ddp22/Desktop/Esame/ChatBot/ROS/src/camera_pkg/src/opencv_face_detector_uint8.pb'
        self._faceNet = cv2.dnn.readNet(faceModel, faceProto)

        # Initialize emotion classifier
        emotionModel = "/home/ddp22/Desktop/Esame/ChatBot/ROS/src/camera_pkg/src/emotion.hdf5"
        self._emotionNet = load_model(emotionModel)
        self._emotionList = ['surprise','fear','disgust','happiness','sadness','anger','neutral']
        self._padding = 0.2
        self._MEANS=np.array([131.0912, 103.8827, 91.4953])
        self._INPUT_SIZE = (224,224)
        print("\n---- EMOTION NODE READY ---\n")



    def getFaceBox(self, net, frame, conf_threshold=0.8):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        
        #swapRB =True
        # flag which indicates that swap first and last channels in 3-channel image is necessary.
        #crop = False
        # flag which indicates whether image will be cropped after resize or not
        # If crop is false, direct resize without cropping and preserving aspect ratio is performed
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold and detections[0, 0, i, 5]<1 and detections[0, 0, i, 6]<1:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/300)), 8)
        return frameOpencvDnn, bboxes
    
    def getEmotion(self, frame):
        frameFace, bboxes = self.getFaceBox(self._faceNet, frame)     # Get face
        emotion = []
        for i,bbox in enumerate(bboxes):  # per ogni volto individuato 
            # Adjust crop
            w = bbox[2]-bbox[0]
            h = bbox[3]-bbox[1]
            padding_px = int(self._padding*max(h,w))
            face = frame[max(0,bbox[1]-padding_px):min(bbox[3]+padding_px,frame.shape[0]-1),max(0,bbox[0]-padding_px):min(bbox[2]+padding_px, frame.shape[1]-1)]
            face = face[ face.shape[0]//2 - face.shape[1]//2 : face.shape[0]//2 + face.shape[1]//2, :, :]
            # Preprocess image
            resized_face = cv2.resize(face,self._INPUT_SIZE)
            blob = np.array([resized_face.astype(float)-self._MEANS])
            # Predict
            emotionPreds = self._emotionNet.predict(blob)
            emotion.append(self._emotionList[emotionPreds[0].argmax()])
            # print('\n\n --- RISULTATO --- \nEmozione: '+str(emotion)+'\n-------------------\n')
        return emotion




# emo_extr = EmotionExtractor()


# # webcam
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Errore: camera non aoerta correttamente.")
#     exit()

# while cap.isOpened():
#     # frame
#     ret, frame = cap.read()
#     if not ret:
#         print("Errore: frame non letto.")
#         break
#     # frame processing
#     emotion = emo_extr.getEmotion(frame)
#     if len(emotion)>0:
#         print('emozione: '+str(emotion[0]))
#     # Break 
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     # sleep 
#     time.sleep(0.5)

# # Release resources
# cap.release()
# cv2.destroyAllWindows()




## Test 
# emo_extr = EmotionExtractor()
# frame = cv2.imread('test4.jpg')                     
# emotion = emo_extr.getEmotion(frame)
# print('emozione: '+str(emotion[0]))



