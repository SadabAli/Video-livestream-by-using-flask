from flask import Flask , render_template , request , url_for , Response
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0)

def Genereate_Image():
    while True:
        # .read() in OpenCV returns 2 things, boolean and data
        success,Image =camera.read()
        if not success:
            break
        else:
            #The cv2.imencode() function in OpenCV is used to encode an image into a specific format (such as JPEG, PNG, etc.) and store it in a memory buffer. This is useful for saving an image to a file or for streaming images over a network.

            # 'ret' is boolean
            #Checking the ret value is important to ensure that the encoding process was successful before proceeding with further operations. For instance, if you try to use the buffer without verifying that ret is True, you might encounter errors or unexpected behavior if the encoding failed.
            ret , buffer =cv2.imencode(".png" , Image)

            # converting buffer back to byte
            Image=buffer.tobytes()

            # byte to img
            yield(b'--Image\r\n'
                   b'Content-Type: image/png\r\n\r\n' + Image + b'\r\n')
            
    



@app.route("/")
def display():
    return render_template("index.html")



@app.route("/video")
def video():
    return Response(Genereate_Image() , mimetype='multipart/x-mixed-replace; boundary=Image')



if __name__=="__main__":
    app.run(debug=True)