# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import ntpath
import os
from pathlib import Path
import cv2
from flask import Flask, redirect, url_for, request, render_template, render_template_string, Response
import numpy as np
from easy_facial_recognition import easy_face_reco, encode_face
import PIL.Image

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
video_capture = None

# INIT
def get_known_face_names():
  print('[INFO] Importing faces...')
  face_to_encode_path = Path('./known_faces')
  files = [file_ for file_ in face_to_encode_path.rglob('*.jpg')]
  for file_ in face_to_encode_path.rglob('*.png'):
    files.append(file_)
  if len(files)==0:
    raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
  return [os.path.splitext(ntpath.basename(file_))[0] for file_ in files], files

def get_known_face_encodings(files):
  known_face_encodings = []
  for file_ in files:
      image = PIL.Image.open(file_)
      image = np.array(image)
      try:
        face_encoded = encode_face(image)[0][0]
      except IndexError:
        print('[ERROR] No face detected in {}'.format(file_))
        continue
      known_face_encodings.append(face_encoded)
  print('[INFO] Faces well imported')
  return known_face_encodings


known_face_names, files = get_known_face_names()
known_face_encodings = get_known_face_encodings(files)
#  return known_face_names, known_face_encodings
# / INIT



# success of image upload
@app.route('/success/<name>')
def success(name):
   global known_face_names, known_face_encodings, video_capture
   video_capture = cv2.VideoCapture(0)
   known_face_names, files = get_known_face_names()
   known_face_encodings = get_known_face_encodings(files)
   return 'welcome %s 👋 <br><br><a href="/canva">Click to go to face detection</a>!<br>' % name

@app.route('/')
def index():
    return redirect(url_for('add_known_faces'))

@app.route('/add_known_faces.html')
def add_known_faces():
    return render_template('add_known_faces.html')

@app.route('/upload_known_faces',methods = ['POST'])
def upload_known_faces():
   if request.method == 'POST':
      user = request.form['nm']
      f = request.files['file']
      f.save(os.path.join('./known_faces', user + '.jpg'))
      return redirect(url_for('success', name = user))

def gen():
    print('[INFO] Webcam well started')
    # known_face_encodings, known_face_names = import_faces()
    while True:
      ret, frame = video_capture.read()
      if not ret:
        raise ValueError('[ERROR] No frame read from the webcam')
      print('[INFO] Video capture read')
      easy_face_reco(frame, known_face_encodings, known_face_names)
      cv2.imwrite('t.jpg', frame)
      print('[INFO] File written')
      yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    video_capture.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/canva')
def canva():
    """Video streaming"""
    #return render_template('index.html')
    print('[INFO] Video feed')
    # Call the gen function to generate the video
    return render_template_string('''<html>
<head>
    <title>Video Streaming </title>
</head>
<body>
    <div>
        <h1>Streaming video</h1>
        <img id="img" src="{{ url_for('video_feed') }}">
    </div>
<script >
    var ctx = document.getElementById("canvas").getContext('2d');
    // need only for animated image
    function refreshCanvas(){
        ctx.drawImage(img, 0, 0);
    };
    window.setInterval("refreshCanvas()", 50);
</script>
</body>
</html>''')


# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
    # gen()
    print('[INFO] Starting')
    app.run(port=8080)
