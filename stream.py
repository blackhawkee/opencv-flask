import cv2
import numpy as np 
from keras.models import load_model
# import argparse
# from PIL import Image
import imutils
import pafy
from SendEmail import email_alert
import beepy

def stream_video(param_url):
    # print(url)
    # url = "https://www.youtube.com/watch?v=38hnIitudak"
    # url = "https://www.youtube.com/watch?v=38hnIitudak&ab_channel=ViralFACTORY"
    video = pafy.new(param_url)
    return video.getbest(preftype="mp4")
    # return cv2.VideoCapture(video_mp4.url)
    # return camera

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
# camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture(stream_video().url)
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

model=load_model("./model/saved_model.h5")
def gen_frames(param_url):  # generate frame by frame from camera

    camera = cv2.VideoCapture(stream_video(param_url).url)
    while True:
        imagedump=[]

        for i in range(10):
            _,frame=camera.read()
            # if frame is None:
            #     break
            image = imutils.resize(frame,width=700,height=600)

            frame=cv2.resize(frame, (227,227), interpolation = cv2.INTER_AREA)
            gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
            gray=(gray-gray.mean())/gray.std()
            gray=np.clip(gray,0,1)
            imagedump.append(gray)

        imagedump=np.array(imagedump)

        imagedump.resize(227,227,10)
        imagedump=np.expand_dims(imagedump,axis=0)
        imagedump=np.expand_dims(imagedump,axis=4)

        output=model.predict(imagedump)

        loss=mean_squared_loss(imagedump,output)

        print('loss >>>>>>> ',loss)

        # if loss>0.00068:
        if (loss>0.00051 and loss < 0.00057) or (loss>0.00061):
            # print('Abnormal Event Detected')
            # print(loss)
            # print('Possible theft')
            cv2.putText(image,"Abnormal Event",(100,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
            email_alert()
            beepy.beep(sound=4)
        
        ret, buffer_data = cv2.imencode('.jpg', image)
        image = buffer_data.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')  # concat frame one by one and show result

def mean_squared_loss(x1,x2):
    difference=x1-x2
    a,b,c,d,e=difference.shape
    n_samples=a*b*c*d*e
    sq_difference=difference**2
    diff_sum=sq_difference.sum()
    distance=np.sqrt(diff_sum)
    mean_distance=distance/n_samples

    return mean_distance