from deepface import DeepFace
from PIL import Image
import os, os.path
import statistics
from . import video

def analyze_video():
    print("Started")
    video.record_video()
    print("Reading images")
    imgs = []
    path = "C:\\Users\\dhrum\\Desktop\\IPD_backend\\PythonModules"
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path,f)))
    print(len(imgs))

    emotions=[]
    print("Performing operations images")
    for i in range(len(imgs)):
        obj = DeepFace.analyze(img_path = imgs[i].filename, actions = ['emotion'],enforce_detection=False)
        emot=obj['dominant_emotion']
        emotions.append(emot)
        
    print(f"Dominant Emotion of datasets : {statistics.mode(emotions)}")

analyze_video()
