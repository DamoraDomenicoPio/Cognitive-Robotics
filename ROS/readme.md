### Per lanciare speech recognition
roslaunch ros_audio_pkg speech_recognition.launch

### Per lanciare rasa ros
roslaunch rasa_ros_pkg dialogue.launch

### Per connettersi a pepper
roslaunch connection_pkg pepper_bringup.launch nao_ip:=192.168.0.103

### Per lanciare tts
roslaunch tts_pkg tts.launch

### Per lanciare respeaker
roslaunch respeaker_pkg respeaker.launch

### Per lanciare il tablet
roslaunch tablet_pkg pepper_bringup.launch

### Per lanciare flask
roslaunch flask_pkg flask.launch

## Per lanciare face tracking
roslaunch face_tracking face_tracking.launch

### Installazioni
pip3 install pyusb
pip3 install flask
sudo apt install net-tools

### Non sono sicuro sia necessario
#pip3 install webrtcvad
#pip3 install respeaker
