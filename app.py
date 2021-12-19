# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import ntpath
import os
from pathlib import Path
import cv2
from flask import Flask, redirect, url_for, request, render_template
import numpy as np
from easy_facial_recognition import easy_face_reco, encode_face
import PIL.Image

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'Hello World'

def gfg():
    return 'geeksforgeeks'

@app.route('/hello/<name>')
def hello_name(name):
   return '👋 Hello %s!' % name

@app.route('/success/<name>')
def success(name):
   return 'welcome %s 👋' % name
 
@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/facial')
def facial():
    print('[INFO] Importing faces...')
    face_to_encode_path = Path('./known_faces')
    files = [file_ for file_ in face_to_encode_path.rglob('*.jpg')]

    for file_ in face_to_encode_path.rglob('*.png'):
        files.append(file_)
    if len(files)==0:
        raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
    known_face_names = [os.path.splitext(ntpath.basename(file_))[0] for file_ in files]

    known_face_encodings = []
    for file_ in files:
        image = PIL.Image.open(file_)
        image = np.array(image)
        face_encoded = encode_face(image)[0][0]
        known_face_encodings.append(face_encoded)

    print('[INFO] Faces well imported')
    print('[INFO] Starting Webcam...')
    video_capture = cv2.VideoCapture(0)
    print('[INFO] Webcam well started')
    print('[INFO] Detecting...')
    while True:
        ret, frame = video_capture.read()
        easy_face_reco(frame, known_face_encodings, known_face_names)
        cv2.imshow('Easy Facial Recognition App', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print('[INFO] Stopping System')
    video_capture.release()
    cv2.destroyAllWindows()

    return render_template('facial.html')



app.add_url_rule('/ici', 'g2g', gfg)

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
    app.run(debug = True)
