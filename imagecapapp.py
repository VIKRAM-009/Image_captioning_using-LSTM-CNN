# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:24:46 2025

@author: vicky

"""
"""Image Captioning project using CNN ans LSTM Streamlit APP part"""
#pip install tensorflow numpy pandas matplotlib pillow nltk tqdm
import streamlit as st
import numpy as np
import pickle
import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the trained model and tokenizer
model = load_model("image_captioning_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("image_features.pkl", "rb") as f:
    image_features = pickle.load(f)

# Load InceptionV3 model for feature extraction
inception_model = InceptionV3(weights="imagenet")
cnn_model = tf.keras.Model(inputs=inception_model.input, outputs=inception_model.layers[-2].output)

# Function to preprocess image
def extract_features(image):
    image = image.resize((299, 299))  # Resize to match InceptionV3 input size
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    features = cnn_model.predict(image)
    return features

# Function to generate caption
def generate_caption(image):
    features = extract_features(image)
    max_length = 35  # Use the same max length from training
    caption = "startseq"

    for _ in range(max_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences([sequence], maxlen=max_length, padding="post")
        y_pred = model.predict([features, sequence])
        word_index = np.argmax(y_pred)
        word = tokenizer.index_word.get(word_index, "")

        if word == "endseq" or word == "":
            break

        caption += " " + word

    return caption.replace("startseq", "").replace("endseq", "").strip()

# Streamlit UI
st.title("🖼️ Image Captioning App")
st.write("Upload an image, and the AI will generate a caption!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        caption = generate_caption(image)
        st.success("**Caption:** " + caption)
