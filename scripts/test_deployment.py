import requests
import cv2
import os, json
import urllib

def rgb2gray(rgb):
    """Convert the input image into grayscale"""
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def resize_img(img_to_resize):
    """Resize image to MNIST model input dimensions"""
    r_img = cv2.resize(img_to_resize, dsize=(28, 28), interpolation=cv2.INTER_AREA)
    r_img.resize((1, 1, 28, 28))
    return r_img

def preprocess(img_to_preprocess):
    """Resize input images and convert them to grayscale."""
    if img_to_preprocess.shape == (28, 28):
        img_to_preprocess.resize((1, 1, 28, 28))
        return img_to_preprocess
    
    grayscale = rgb2gray(img_to_preprocess)
    processed_img = resize_img(grayscale)
    return processed_img


urllib.urlretrieve ("https://user-images.githubusercontent.com/379372/31909713-d9046856-b7ef-11e7-98fe-8a1e133c0010.png", "test.png")
test_image = "test.png"

img = mpimg.imread(test_image)
print("Old Dimensions: ", img.shape)
img = preprocess(img)

input_data = json.dumps({'data': img.tolist()})
service=Webservice(name ='aciwebservice', workspace =ws)

try:
    r = service.run(input_data)
    result = r['result']
    time_ms = np.round(r['time_in_sec'] * 1000, 2)
except KeyError as e:
    print(str(e))
