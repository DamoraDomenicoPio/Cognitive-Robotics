#!/usr/bin/env python3

import os
import rospy
from rasa_ros_pkg.srv import Dialogue, DialogueResponse
from std_msgs.msg import String
import subprocess

class TerminalInterface:
    '''Class implementing a terminal i/o interface. 

    Methods
    - get_text(self): return a string read from the terminal
    - set_text(self, text): prints the text on the terminal

    '''

    def get_text(self):
        return input("[IN]:  ") 

    def set_text(self,text):
        print("[OUT]:",text)

# def main():
#     rospy.init_node('writing')
#     rospy.wait_for_service('dialogue_server')
#     dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)
#     print("connesso al server")
#     print(os.getcwd())

#     terminal = TerminalInterface()

#     while not rospy.is_shutdown():
#         message = terminal.get_text()
#         if message == 'exit': 
#             break
#         try:
#             bot_answer = dialogue_service(message)
#             terminal.set_text(bot_answer.answer)
#             path = '../Desktop/Progetto/src/rasa_ros_pkg/scripts/tts.sh'
#             subprocess.run(['bash', path, str(bot_answer.answer)])
#         except rospy.ServiceException as e:
#             print("Service call failed: %s"%e)



dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)

def callback(text):
    print("Dentro la callback")
    message = "[IN]:  " + str(text.data)
    print(message)
    bot_answer = dialogue_service(text.data)
    print("[OUT]:",bot_answer.answer)
    
    data_to_send = String()
    data_to_send.data = bot_answer.answer
    pub.publish(data_to_send)
    
    # path = '/src/rasa_ros_pkg/scripts/tts.sh'
    # print(str(bot_answer.answer))
    # subprocess.run(['bash', path, str(bot_answer)])

pub = rospy.Publisher('tts_pepper', String, queue_size=10)

def main():
    rospy.init_node('writing')
    rospy.wait_for_service('dialogue_server')
    print("connesso al server")
    
    rospy.Subscriber("voice_txt", String, callback)
    rospy.spin()

if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass