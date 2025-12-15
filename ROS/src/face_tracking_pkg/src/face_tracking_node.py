#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

from utils import Session
from optparse import OptionParser
import rospy
import time
from std_msgs.msg import String, Float32MultiArray, Int16

tracking = True
emotion = None
direction = 1
num_persons = 0

class FaceTrackingNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._session = Session(ip, port)
        self._motion_service = self._session.get_service("ALMotion")
        self._tracker_service = self._session.get_service("ALTracker")

        ###
        # self._people_perception = self._session.get_service("ALPeoplePerception")
        ###

    def get_motion_service(self):
        return self._motion_service
    
    def get_tracker_service(self):
        return self._tracker_service

    def start(self, faceSize):
        """
        This example shows how to use ALTracker with face.
        """
        
        rospy.init_node("face_tracking_node")
        
        
        # First, wake up.
        self.get_motion_service().wakeUp()

        # Add target to track.
        targetName = "Face"
        faceWidth = faceSize
        self.get_tracker_service().registerTarget(targetName, faceWidth)

        # Then, start tracker.
        self.get_tracker_service().track(targetName)

        ###
        pub1 = rospy.Publisher('/head_rotation/yaw', Float32MultiArray, queue_size=1)
        pub2 = rospy.Publisher('/head_rotation/pitch', Float32MultiArray, queue_size=1)
        pub3 = rospy.Publisher("tts_pepper", String, queue_size=1)
        ###


        print ("ALTracker successfully started, now show your face to robot!")
        print ("Use Ctrl+c to stop this script.")

        velocity = 0.15
        happiness_sentece = "hi, I'm pepper. You seem happy. How can I help you?"
        sadness_sentence = "hi, I'm pepper. You seem sad. How can I help you cheer you up?"
        surprise_sentece ="hi, I'm pepper. You seem surprise. How can I help you?"
        k = 0
        person_is_tracked = False
        msg = Float32MultiArray()
        msg.data = [0.0, velocity]

        try:
            # global tracking
            while True:
                time.sleep(1)
                if k > 2:
                    pub1.publish(msg)
                    pub2.publish(msg)
                if tracking:
                    #print(tracking)
                    
                    if emotion == "happiness" and num_persons == 1:
                        if person_is_tracked == False:
                            pub3.publish(happiness_sentece)
                            print("Say that you are happy")
                        person_is_tracked = True
                        self.get_tracker_service().track(targetName)
                        k = 0
                    elif emotion=="surprise" and num_persons == 1:
                        if person_is_tracked == False:
                            pub3.publish(surprise_sentece)
                            print("Say that you are surprise")
                        person_is_tracked = True
                        self.get_tracker_service().track(targetName)
                        k = 0
                    elif emotion=="noface" or num_persons != 1:
                        k = k + 1
                        print("No face")
                        if k > 2:
                            person_is_tracked = False
                            self.get_tracker_service().stopTracker()
                    else:
                        if person_is_tracked == False:
                            pub3.publish(sadness_sentence)
                            print("Say that you are sad")
                        person_is_tracked = True
                        self.get_tracker_service().track(targetName)
                        k = 0
                else:
                    self.get_tracker_service().stopTracker()
                    k = k + 1

        except KeyboardInterrupt:
            print()
            print("Interrupted by user")
            print("Stopping...")

        # Stop tracker.
        self.get_tracker_service().stopTracker()
        self.get_tracker_service().unregisterAllTargets()
        self.get_motion_service().rest()

        print("ALTracker stopped.")

def callback(data):
    global tracking
    if data.data == "follow me":
        tracking = True
    else:
        tracking = False

# def callback_direction(data):
#     global direction
#     if data.data < 90:
#         # right
#         data = 1
#     else:
#         # left
#         data = -1
def callback_emotions(data):
    global emotion
    global num_persons
    try:
        values = data.data.split("/")
        emotion = values[1]
        num_persons = len(values)-1

    except:
        emotion = "noface"
        num_persons = 0
    return emotion


if __name__ == "__main__":
        rospy.Subscriber("face_tracking_start_stop", String, callback)
        rospy.Subscriber("emotions", String, callback_emotions)
        ###
        #rospy.Subscriber("direction_head_motion", Int16, callback_direction)
        ###
        parser = OptionParser()
        parser.add_option("--ip", dest="ip", default="10.0.1.207")
        parser.add_option("--port", dest="port", default=9559)
        (options, args) = parser.parse_args()
        try:
            ftn = FaceTrackingNode(options.ip, int(options.port))
            ftn.start(0.1)
        except rospy.ROSInterruptException:
            pass
