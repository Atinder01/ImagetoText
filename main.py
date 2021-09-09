import streamlit as st
import pytesseract
import cv2
from PIL import Image
import numpy as np

def credits(content):
    st.markdown(
        f'<p style="color:{"#0796B6"};">{content}</p>',
        unsafe_allow_html=True)

new_title = '<p style="font-family:sans-serif; color:#0796B6; font-size: 42px; text-align: center">GET TEXT FROM IMAGE</p>'
st.markdown(new_title, unsafe_allow_html=True)
#st.title("GET TEXT FROM IMAGE")
image = Image.open("image2text.png")
st.image(image, use_column_width=True)

pytesseract.pytesseract.tesseract_cmd = "tesseract"
credits("""
If you want to find out how to turn an image into a text document, you came to the right place. This free online tool allows you to convert from image to text.
Upload the image from which you need to extract text
""")
uploaded_file = st.file_uploader("")
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    credits("")
    credits("Getting text...")
    hImg,wImg,_=img.shape
    boxes = pytesseract.image_to_data(img)
    t = pytesseract.image_to_string(img)
    for x,b in enumerate(boxes.splitlines()):
      if x!=0:
        b=b.split()
        if(len(b)==12):
            x,y,w,h=int(b[6]),int(b[7]),int(b[8]),int(b[9])
            cv2.rectangle(img,(x,y),(w+x,h+y),(50,50,50),1)
            cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
            #try:
            #    pdf.cell(200, 10, b[11])
            #except UnicodeEncodeError:
            #   pdf.cell(200,10," ")
    st.image(img, caption='Text in your image.', use_column_width=True, clamp=True)
    credits("Text in your image goes here: ")
    st.write(t)

st.text("")
st.text("")
credits("Made By:")
credits("Atinderpal Kaur")
credits("101803176")
credits("COE-9")
