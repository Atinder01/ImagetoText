import streamlit as st
import pytesseract
import cv2
from PIL import Image
import numpy as np

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def credits(content):
    st.markdown(
        f'<p style="color:{"#0796B6"};">{content}</p>',
        unsafe_allow_html=True)
    
image = Image.open("image2text.png")
st.image(image, use_column_width=True)
new_title = '<p style="font-family:sans-serif; color:#0796B6; font-size: 32px; text-align: center">GET TEXT FROM IMAGE</p>'
st.markdown(new_title, unsafe_allow_html=True)

pytesseract.pytesseract.tesseract_cmd = "tesseract"
credits("""
If you want to find out how to turn an image into a text document, you came to the right place. This free online tool allows you to convert from image to text.
Upload the image from which you need to extract text
""")
file = st.file_uploader("")
if file is not None:
  try:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    #img=deskew(img)
    #ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
    #img=cv2.medianBlur(img,5)
    #img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hImg,wImg,_=img.shape
    boxes = pytesseract.image_to_data(img)
    t = pytesseract.image_to_string(img)
    flag=0
    for x,b in enumerate(boxes.splitlines()):
      if x!=0:
        b=b.split()
        if(len(b)==12):
            flag=1
            x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,h+y),(50,50,50),1)
            cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
    st.image(img, caption='Text in your image.', use_column_width=True, clamp=True)
    if flag==1:
        credits("Text in your image goes here: ")
        st.write(t)
    else:
        st.write("No text found")
  except:
    error = '<p style="font-family:sans-serif; color:red; font-size: 22px; ">Invalid file uploaded!</p><p style="font-family:sans-serif; color:red; font-size: 22px; ">Please upload a valid file.</p>'
    st.markdown(error, unsafe_allow_html=True)

st.text("")
st.text("")
credits("Made By:")
credits("Atinderpal Kaur")
credits("101803176")
credits("COE-9")
st.text("")
st.text("")
