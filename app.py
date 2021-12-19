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
video_capture = cv2.VideoCapture(0)

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


def gen():
    print('[INFO] Webcam well started')
    while True:
      ret, image = video_capture.read()
      print('[INFO] Video capture read')
      cv2.imwrite('t.jpg', image)
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
        <h1>Image</h1>
        <img id="img" src="{{ url_for('video_feed') }}">
    </div>
    <div>
        <h1>Canvas</h1>
        <canvas id="canvas" width="640px" height="480px"></canvas>
    </div>

<script >
    var ctx = document.getElementById("canvas").getContext('2d');
    var img = new Image();
    img.src = "{{ url_for('video_feed') }}";

    // need only for static image
    //img.onload = function(){
    //    ctx.drawImage(img, 0, 0);
    //};

    // need only for animated image
    function refreshCanvas(){
        ctx.drawImage(img, 0, 0);
    };
    window.setInterval("refreshCanvas()", 50);

</script>

</body>
</html>''')


app.add_url_rule('/ici', 'g2g', gfg)

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
    gen()
    print('[INFO] Generation OK')
    app.run(debug = True)
