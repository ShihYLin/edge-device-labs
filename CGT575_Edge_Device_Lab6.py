import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
import folium
from exif import Image as exif
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
from PIL import Image

# Deep learning libraries
from keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input,decode_predictions
st.title('CGT575 / ASM591 Lab 6')

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees

# SIDEBAR
task = st.sidebar.selectbox("Select Task: ", ("Homepage", "Deep Learning", "Mapping", "Homework", "Object Detection"))
st.write(task)

 # PAGE
def pages(task):
    if task == "Homepage":
        st.title('Lab 6')
        lat = 40.424146
        lon = -86.918105
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data)

    elif task == "Deep Learning":

        st.title(task)
        model = VGG16(weights = 'imagenet')
        img_path = 'maxwell.jpg'
        img = image.load_img(img_path, color_mode='rgb', target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        p = decode_predictions(features)
        
        st.image(img)

        for preds in p[0]:
            st.write('The image is ' + preds[1] + ' with probability: ' + str(preds[2]))
        
        # Allow user to upload files
        uploaded_file = st.file_uploader("Upload Image")
        if uploaded_file is not None:

            # Display the image
            display_image = Image.open(uploaded_file)
            st.image(display_image)

            # Resize the image for tensorflow prediction
            temp_img = display_image.resize((224, 224), Image.ANTIALIAS)
            img_tensor = tf.keras.preprocessing.image.img_to_array(temp_img)
            img_tensor = np.expand_dims(img_tensor, axis = 0)
            img_tensor /= 255

            # Use the deep learning model to make the prediction and highlight the section of the image
            prediction = model.predict(img_tensor)
            p2 = decode_predictions(prediction)
            for preds in p2[0]:
                st.write('The image is ' + preds[1] + ' with probability: ' + str(preds[2]))
    
    elif task == "Mapping":

        st.title(task)
        lat = 40.424146
        lon = -86.918105
        m = folium.Map (location = [lat,lon], zoom_start=15)
        folium.Marker([lat, lon], popup='Field', tooltip='Diseased Field').add_to(m)

        # how to show map on the webapplication
        folium_static(m)

    elif task == "Homework":

        st.title(task)
        # Allow user to upload files
        uploaded_file = st.file_uploader("Upload Image")
        if uploaded_file is not None:

            # Display the image
            #display_image = Image.open(uploaded_file)
            st.image(uploaded_file)
            img = exif(uploaded_file)
            coords = (decimal_coords(img.gps_latitude, img.gps_latitude_ref), decimal_coords(img.gps_longitude, img.gps_longitude_ref))
            #lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
            #lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)
            # Mark on map
            m = folium.Map(location = [coords[0],coords[1]], zoom_start=15)
            folium.Marker([coords[0],coords[1]], popup='Field', tooltip='Diseased Field').add_to(m)
            folium_static(m)

    elif task == "Object Detection":
        
        st.title(task)
        image1 = Image.open('detection2.png')
        image2 = Image.open('detection3.png')
        image3 = Image.open('detection4.png')
        image4 = Image.open('detection5.png')
        image5 = Image.open('detection6.png')
        st.image(image1)
        st.image(image2)
        st.image(image3)
        st.image(image4)
        st.image(image5)
pages(task)