#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String, Int16
import numpy as np

from speech_recognition import AudioData
import speech_recognition as sr
from tuning import Tuning
import usb.core
import usb.util
import time
import num2words
# Initialize a Recognizer
r = sr.Recognizer()

# Init node
rospy.init_node('speech_recognition', anonymous=True)
pub1 = rospy.Publisher('voice_data', Int16MultiArray, queue_size=10)
pub2 = rospy.Publisher('voice_txt', String, queue_size=10)
pub3 = rospy.Publisher('face_tracking_start_stop', String, queue_size=10)
pub4 = rospy.Publisher('tts_pepper', String, queue_size=10)

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
Mic_tuning = None
if dev:
    print("Dispositivo trovato")
    Mic_tuning = Tuning(dev)
else:
    print("dispositivo non trovato")

def n2w(sentence):
    sentence_list = sentence.split(" ")
    for i in range(len(sentence)):
        try:
            k = num2words.num2words(int(sentence_list[i]))
            
            sentence_list[i] = str(k)
        except:
            pass
    
    sentence = " ".join(sentence_list)
    print(sentence)
    return sentence

# this is called from the background thread
def callback(audio):
    data = np.array(audio.data,dtype=np.int16)
    audio_data = AudioData(data.tobytes(), 16000, 2)

    try:
        spoken_text= r.recognize_google(audio_data, language='en-EN')
        print("Google Speech Recognition pensa tu abbia detto: " + spoken_text)
        pub1.publish(audio) # Publish audio only if it contains words
        direction = Mic_tuning.direction
        print(direction)

        if direction > 180 and direction< 360:
            pub4.publish("Stand in front of me, please")
        elif spoken_text.lower() == "follow me" or spoken_text.lower() == "don't follow me anymore":
            pub3.publish(spoken_text)
            ###
            # pub5.publish(direction)
            ###
        else:
            pub2.publish(n2w(spoken_text))
            ###
            # pub5.publish(direction)
            ###


        # if spoken_text.lower() == "follow me" or spoken_text.lower() == "don't follow me anymore":
        #     pub3.publish(spoken_text)
        #     ###
        #     # pub5.publish(direction)
        #     ###
        # else:
        #     pub2.publish(n2w(spoken_text))
        #     ###
        #     # pub5.publish(direction)
        #     ###
    except sr.UnknownValueError:
        print("Google Speech Recognition non riesce a capire da questo file audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listener():
    rospy.Subscriber("mic_data", Int16MultiArray, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
