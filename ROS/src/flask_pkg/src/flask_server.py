#!/usr/bin/env python

# from flask import Flask, render_template, request
# from std_msgs.msg import String  # Importa la classe String da std_msgs.msg

# app = Flask(__name__)

# def handle_request():
#     # Ottenere i dati inviati con la richiesta POST
#     data = request.json  # Supponendo che i dati siano inviati in formato JSON

#     # Esempio di pubblicazione di un messaggio ROS
#     message = data.get('message', '')  # Modificare in base alla struttura dei dati inviati
#     pub.publish(String(message))

#     return "OK"

# @app.route('/', methods=['GET', 'POST', 'OPTIONS'])
# def index():
#     if request.method == 'POST':
#         return handle_request()
#     return render_template('index.html')

# if __name__ == "__main__":
#     from flask_cors import CORS
#     import rospy

#     app.add_url_rule('/', 'handle_request', handle_request, methods=['POST', 'OPTIONS'])
#     rospy.init_node("flask_node")
#     pub = rospy.Publisher('voice_txt', String, queue_size=1)

#     # Abilita CORS per consentire le richieste da origini diverse
#     CORS(app)

#     app.run(host='0.0.0.0', port=8080)
#     print("Server running...")















# #!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify

import requests
import rospy
from std_msgs.msg import String

app = Flask(__name__)

def make_sentence(data):
    sentence = "How many people "
    k = 0
    for i in data:
        key = list(i.keys())[0]
        if key == "gender":
            sentence = sentence.replace("people", i[key])
            k = k - 1
        elif key == "upper_color":
            if k > 0:
                sentence = sentence + " and "
            if i[key].startswith("not_"):
                sentence = sentence + "aren't wearing " + i[key][len("not_"):] + " shirts"
            else:
                sentence = sentence + "are wearing " + i[key] + " shirts"
        elif key == "lower_color":
            if k > 0:
                sentence = sentence + " and "
            if i[key].startswith("not_"):
                sentence = sentence + "aren't wearing " + i[key][len("not_"):] + " jeans"
            else:
                sentence = sentence + "are wearing " + i[key] + " jeans"
        elif key == "hat":
            if k > 0:
                sentence = sentence + " and "
            if i[key] == "true":
                sentence = sentence + "are wearing hats"
            else:
                sentence = sentence + "are not wearing hats"
        elif key == "bag":
            if k > 0:
                sentence = sentence + " and "
            if i[key] == "true":
                sentence = sentence + "are wearing bags"
            else:
                sentence = sentence + "are not wearing bags"
        elif key == "location":
            if k > 0:
                sentence = sentence + " and "
            sentence = sentence + "are presents in " + i[key]
        k = k + 1
    if k == 0:
        sentence = sentence + "are there"
    return sentence + "?"


def handle_request():
    if request.method == 'OPTIONS':
        # Il client sta effettuando una richiesta OPTIONS, rispondi con le informazioni necessarie
        response = app.make_default_options_response()
    elif request.method == 'POST':
        # Il client sta effettuando una richiesta POST, gestisci i dati inviati
        data = request.get_json()
        #print("Dati ricevuti:", data)
        sentence = make_sentence(data)
        print(sentence)
        pub.publish(sentence)
        response = jsonify({"message": "Dati ricevuti con successo"})
        #requests.post("http://172.31.37.236:5002/webhooks/rest/webhook", json ={"sender": "bot","message": sentence})
        
    else:
        # Gestione di altri metodi, ad esempio GET
        response = jsonify({"message": "Metodo non supportato"})

    # Configura gli header CORS (Cross-Origin Resource Sharing)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.add_url_rule('/', 'handle_request', handle_request, methods=['POST', 'OPTIONS'])
    rospy.init_node("tts_pepper")
    pub = rospy.Publisher('voice_txt', String, queue_size=1)
    app.run(host='0.0.0.0', port=5000)
