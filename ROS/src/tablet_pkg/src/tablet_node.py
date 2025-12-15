#!/usr/bin/python3

# import rospy
# from tablet_pkg.srv import LoadUrl, LoadUrlRequest, LoadUrlResponse

# class Handler:
#     '''
#     The constructor creates the service proxy object, which is able to display the desired URL on the tablet.
#     '''
#     def __init__(self):
#         self.tablet_service = None
#         # self.tablet_service = rospy.ServiceProxy("load_url", LoadUrl)

#     '''
#     This method calls the tablet service and sends it the URL of the web page to be displayed.
#     '''
#     def load_url(self, url):
#         msg = LoadUrlRequest()
#         msg.url = url
#         self.tablet_service = rospy.ServiceProxy("load_url", LoadUrl)
#         resp = self.tablet_service(msg)
#         rospy.loginfo(resp.ack)

# if __name__ == "__main__":
#     NODE_NAME = "table_node_example"
#     rospy.init_node(NODE_NAME)
#     handler = Handler()
#     url = r"https://www.diem.unisa.it/"
#     handler.load_url(url)

import rospy
from tablet_pkg.srv import LoadUrl, LoadUrlRequest, LoadUrlResponse

class Handler:
    '''
    The constructor creates the service proxy object, which is able to display the desired URL on the tablet.
    '''
    def __init__(self):
        self.tablet_service = None
        


    '''
    This method calls the tablet service and sends it the URL of the web page to be displayed.
    '''
    def load_url(self, url):
        print(url)
        msg = LoadUrlRequest()
        msg.url = url
        self.tablet_service = rospy.ServiceProxy("load_url", LoadUrl)
        resp = self.tablet_service(msg)
        rospy.loginfo(resp.ack)


    def load_response(self, url):
        msg = LoadUrlResponse()
        msg.url = url
        self.tablet_service = rospy.ServiceProxy("load_url", LoadUrl)
        resp = self.tablet_service(msg)
        rospy.loginfo(resp.ack)

if __name__ == "__main__":
    NODE_NAME = "table_node"
    rospy.init_node(NODE_NAME)
    handler = Handler()
    #url = r"https://www.diem.unisa.it/"
    url = r"http://10.0.1.109:8080/"
    print("Load")
    handler.load_url(url)
    rospy.spin()








# from utils import Session
# from optparse import OptionParser
# import rospy
# from tablet_pkg.srv import ExecuteJS, LoadUrl

# '''
# This class implements a ROS node used to controll the Pepper tablet
# '''
# class TabletNode:
    
#     '''
#     The costructor creates a session to Pepper and inizializes the services
#     '''
#     def __init__(self, ip, port):
#         self.ip = ip
#         self.port = port
#         self.session = Session(ip, port)
#         self.tablet_proxy = self.session.get_service("ALTabletService")
#         self.tablet_proxy.resetTablet()
    
#     '''
#     It receives a LoadUrl message and displays the web page associated with the url on the tablet.
#     '''
#     def load_url(self, msg):
#         try:
#             self.tablet_proxy.showWebview(msg.url)
#         except:
#             self.tablet_proxy = self.session.get_service("ALTabletService")
#             self.tablet_proxy.showWebview(msg.url)
#         return "ACK"
    
#     '''
#      It receives a LoadUrl message and executes the javascript on the web browser
#     '''
#     def execute_js(self, msg):
#         try:
#             self.tablet_proxy.executeJS(msg.js)
#         except:
#             self.tablet_proxy = self.session.get_service("ALTabletService")
#             self.tablet_proxy.executeJS(msg.js)
            
#         return "ACK"
    
#     '''
#     Starts the node and creates the services
#     '''
#     def start(self):
#         rospy.init_node("tablet_node")

#         rospy.Service('execute_js', ExecuteJS, self.execute_js)
#         rospy.Service('load_url', LoadUrl, self.load_url)

#         rospy.spin()

# if __name__ == "__main__":
#     parser = OptionParser()
#     parser.add_option("--ip", dest="ip", default="10.0.1.207")
#     parser.add_option("--port", dest="port", default=9559)
#     (options, args) = parser.parse_args()

#     try:
#         node = TabletNode(options.ip, int(options.port))
#         node.load_url(r'http://10.0.2.15:8080/')
#         node.start()
#     except rospy.ROSInterruptException:
#         pass











# from utils import Session
# from optparse import OptionParser
# import rospy
# from tablet_pkg.srv import ExecuteJS, LoadUrl
# from std_msgs.msg import String

# '''
# This class implements a ROS node used to controll the Pepper tablet
# '''
# class TabletNode:
    
#     '''
#     The costructor creates a session to Pepper and inizializes the services
#     '''
#     def __init__(self, ip, port):
#         self.ip = ip
#         self.port = port
#         self.session = Session(ip, port)
#         self.tablet_proxy = self.session.get_service("ALTabletService")
#         self.tablet_proxy.resetTablet()
    
#     '''
#     It receives a LoadUrl message and displays the web page associated with the url on the tablet.
#     '''
#     def load_url(self, msg):
#         try:
#             self.tablet_proxy.showWebview("tablet_pkg/src/index.html")
#             # self.tablet_proxy.showWebview(msg.url)
#         except:
#             self.tablet_proxy = self.session.get_service("ALTabletService")
#             self.tablet_proxy.showWebview(msg.url)
#         return "ACK"
    
#     '''
#      It receives a LoadUrl message and executes the javascript on the web browser
#     '''
#     def execute_js(self, msg):
#         try:
#             self.tablet_proxy.executeJS(msg.js)
#         except:
#             self.tablet_proxy = self.session.get_service("ALTabletService")
#             self.tablet_proxy.executeJS(msg.js)
            
#         return "ACK"
    
#     '''
#     Starts the node and creates the services
#     '''
#     def start(self):
#         rospy.init_node("tablet_node")

        

#         rospy.Service('execute_js', ExecuteJS, self.execute_js)
#         rospy.Service('load_url', LoadUrl, self.load_url)

#         #rospy.spin()


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# def make_sentence(data):
#     sentence = "How many people "
#     k = 0
#     for i in data:
#         key = list(i.keys())[0]
#         if key == "gender":
#             sentence = sentence.replace("people", i[key])
#             k = k - 1
#         elif key == "upper_color":
#             if k > 0:
#                 sentence = sentence + " and "
#             if i[key].startswith("not_"):
#                 sentence = sentence + "aren't wearing " + i[key][len("not_"):] + " shirts"
#             else:
#                 sentence = sentence + "are wearing " + i[key] + " shirts"
#         elif key == "lower_color":
#             if k > 0:
#                 sentence = sentence + " and "
#             if i[key].startswith("not_"):
#                 sentence = sentence + "aren't wearing " + i[key][len("not_"):] + " jeans"
#             else:
#                 sentence = sentence + "are wearing " + i[key] + " jeans"
#         elif key == "hat":
#             if k > 0:
#                 sentence = sentence + " and "
#             if i[key] == "true":
#                 sentence = sentence + "are wearing hats"
#             else:
#                 sentence = sentence + "are not wearing hats"
#         elif key == "bag":
#             if k > 0:
#                 sentence = sentence + " and "
#             if i[key] == "true":
#                 sentence = sentence + "are wearing bags"
#             else:
#                 sentence = sentence + "are not wearing bags"
#         elif key == "location":
#             if k > 0:
#                 sentence = sentence + " and "
#             sentence = sentence + "are presents in " + i[key]
#         k = k + 1
#     if k == 0:
#         sentence = sentence + "are there"
#     return sentence + "?"


# def handle_request():
#     if request.method == 'OPTIONS':
#         # Il client sta effettuando una richiesta OPTIONS, rispondi con le informazioni necessarie
#         response = app.make_default_options_response()
#     elif request.method == 'POST':
#         # Il client sta effettuando una richiesta POST, gestisci i dati inviati
#         data = request.get_json()
#         #print("Dati ricevuti:", data)
#         sentence = make_sentence(data)
#         print(sentence)
#         pub.publish(sentence)
#         response = jsonify({"message": "Dati ricevuti con successo"})
#     else:
#         # Gestione di altri metodi, ad esempio GET
#         response = jsonify({"message": "Metodo non supportato"})

#     # Configura gli header CORS (Cross-Origin Resource Sharing)
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

#     return response





# if __name__ == "__main__":

#     pub = rospy.Publisher('tts_pepper', String, queue_size=10)
#     app.add_url_rule('/', 'handle_request', handle_request, methods=['POST', 'OPTIONS'])
    

#     parser = OptionParser()
#     parser.add_option("--ip", dest="ip", default="10.0.1.230")
#     parser.add_option("--port", dest="port", default=9559)
#     (options, args) = parser.parse_args()

#     try:
#         node = TabletNode(options.ip, int(options.port))
#         node.load_url("a")
#         node.start()
#     except rospy.ROSInterruptException:
#         pass

#     # rospy.init_node("tablet_node")

#     app.run(host='0.0.0.0', port=8080)



#     # rospy.spin()
