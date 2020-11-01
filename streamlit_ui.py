import streamlit as st
import cv2
import matplotlib.pyplot as plt
import numpy as np
from solve import find_shortest_path, drawPath

st.title('Maze Solving with Dijkstra Algorithm')
file = st.file_uploader('Choose an image', ['jpg', 'jpeg', 'png'])
st.write('Alternatively, ')
use_default = st.checkbox('Use default maze')

img, marked = None, None

if use_default:
    img = cv2.imread('sample.jpg')
elif file is not None:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

if img is not None:
    st.subheader('Use the sliders on the left to position the start and end points')
    start_x = st.sidebar.slider("Start X", value= 24 if use_default  else 50, min_value=0, max_value=img.shape[1], key='sx')
    start_y = st.sidebar.slider("Start Y", value= 332 if use_default  else 100, min_value=0, max_value=img.shape[0], key='sy')
    finish_x = st.sidebar.slider("Finish X", value= 309 if use_default  else 100, min_value=0, max_value=img.shape[1], key='fx')
    finish_y = st.sidebar.slider("Finish Y", value= 330 if use_default  else 100, min_value=0, max_value=img.shape[0], key='fy')
    marked = img.copy()
    thickness=(marked.shape[0] + marked.shape[0])//2//100
    cv2.circle(marked, (start_x, start_y), thickness, (0, 255, 0), -1)
    cv2.circle(marked, (finish_x, finish_y), thickness, (255, 0, 0), -1)
    st.image(marked, channels="RGB", width=800)

if marked is not None:
    if st.button('Solve it!'):
        with st.spinner('Processing...'):
            path = find_shortest_path(img, (start_x, start_y), (finish_x, finish_y))
        pathed = img.copy()
        thickness = (pathed.shape[0] + pathed.shape[0]) // 200
        drawPath(pathed, path, thickness)
        st.image(pathed, channels="RGB", width=800)
