# # File: server.py
# from http.server import SimpleHTTPRequestHandler
# from socketserver import TCPServer

# class MyHandler(SimpleHTTPRequestHandler):
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         data = self.rfile.read(content_length)
#         print(f"Ricevuto dato: {data.decode('utf-8')}")

# if __name__ == "__main__":
#     port = 8080  # Cambia la porta se necessario
#     with TCPServer(("", port), MyHandler) as httpd:
#         print(f"Server in ascolto sulla porta {port}")
#         httpd.serve_forever()

from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

#@app.route('/', methods=['POST', 'OPTIONS'])
# def handle_request():
#     # if request.method == 'OPTIONS':
#     #     # Il client sta effettuando una richiesta OPTIONS, rispondi con le informazioni necessarie
#     #     response = app.make_default_options_response()
#     # elif request.method == 'POST':
#     #     # Il client sta effettuando una richiesta POST, gestisci i dati inviati
#     #     data = request.get_json()
#     #     print("Dati ricevuti:", data)
#     #     #response = jsonify({"message": "Dati ricevuti con successo"})
#     # else:
#     #     # Gestione di altri metodi, ad esempio GET
#     #     response = jsonify({"message": "Metodo non supportato"})

#     # # Configura gli header CORS (Cross-Origin Resource Sharing)
#     # response.headers['Access-Control-Allow-Origin'] = '*'
#     # response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#     # response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

#     # return response
#     data = request.get_json()
#     print("Dati ricevuti:", data)

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
            word = i[key].removeprefix("not_")
            if word == i[key]:
                sentence = sentence + "are wearing " + i[key] + " shirts"
            else:
                sentence = sentence + "aren't wearing " + word + " shirts"
        elif key == "lower_color":
            if k > 0:
                sentence = sentence + " and "
            word = i[key].removeprefix("not_")
            if word == i[key]:
                sentence = sentence + "are wearing " + i[key] + " jeans"
            else:
                sentence = sentence + "aren't wearing " + word + " jeans"
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
        response = jsonify({"message": "Dati ricevuti con successo"})
        # Effettua la chiamata POST
        
        #response1 = requests.post("http://10.0.1.109:8080/receive_message", json={"message":sentence})
        
        # Stampa la risposta del server
        print("Risposta del server:", response1.text)
        #requests.post("http://172.31.37.236:5002/webhooks/rest/webhook", json ={"sender": "bot","message": sentence})
        
    else:
        # Gestione di altri metodi, ad esempio GET
        response = jsonify({"message": "Metodo non supportato"})

    # Configura gli header CORS (Cross-Origin Resource Sharing)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

@app.route('/', methods=['GET'])
def serve_index():
    return render_template('index.html')

if __name__ == "__main__":
    app.add_url_rule('/', 'handle_request', handle_request, methods=['POST', 'OPTIONS'])
    app.run(host='0.0.0.0', port=8080)