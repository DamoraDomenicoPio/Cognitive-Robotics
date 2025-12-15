#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import os
import numpy as np
from EmotionExtractor import EmotionExtractor

'''
This class implements a ROS node that read the video stream published on the specific topic and shows it in a openCV window
'''
class Nodo(object):
    def __init__(self):
        # Params
        self.br = CvBridge()
        self.emo_extr = EmotionExtractor()
        self.emotion_publisher = rospy.Publisher('emotions', String, queue_size=1)  #TODO
    
    '''
    This method receives a Image message and converts it to numpy array, then show the image opening a window
    '''
    def callback(self, msg):
        image = self.br.imgmsg_to_cv2(msg)
        # cv2.imshow("Pepper Camera", image)
        emotions = self.emo_extr.getEmotion(image)
        message = self.emo2str(emotions)
        if len(emotions)>0:
            print('emozione: '+message)   #TODO se non funziona 
        else: 
            print('nessun volto rilevato')
            mess = str('/noface')
        self.emotion_publisher.publish(message)   #TODO
        cv2.waitKey(50)


    def emo2str(self, emotions): 
        message = '' 
        for emotion in emotions:
            message = message+'/'+str(emotion)
        return message
    
    '''
    THis method subscribes the node to specific topic and starts the node loop
    '''
    def start(self):
        # Subscriber
        rospy.Subscriber("/in_rgb", Image, self.callback)

        rospy.spin()


if __name__ == '__main__':
    rospy.init_node("camera_show_node", anonymous=True)
    my_node = Nodo()
    my_node.start()
