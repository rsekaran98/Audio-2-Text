# Audio_to_Text App
# Author : Sekaran Ramalingam
# Company: SeaportAi
# Cleint: for General Client Demo purpose on streamlit
# Date: 17-10-2020

# Importing all the libraries
import streamlit as st
from PIL import Image
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Seaport image
img = Image.open("SeaportAI.jpg")
st.sidebar.image(img,width=70,caption  = ' ')

# Title on HTML
title = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Converting Audio (WAV) file to text</h2>
    </div>
    """
st.markdown(title,unsafe_allow_html=True)

# Notes
st.write("""
## :joy: -------------------------------------------------------:heart: 
#### Author: Sekaran Ramalingam - SeaportAI
""")

fltyp = st.radio(
          "Pls. select the file...",
         ('Small Audio File', 'Large Audio File'))

if fltyp == 'Small Audio File':
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    st.write("Welcome.wav")
    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    # with sr.AudioFile('C://Users//Admin//Desktop//Deep Learning//Welcome.wav') as source:
    with sr.AudioFile('Welcome.wav') as source:
        audio_text = r.listen(source)

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:

            # using google speech recognition
            text = r.recognize_google(audio_text)
            st.write('Converting audio transcripts into text ...')
            st.write(text)

        except:
            st.write('Sorry.. run again...')


if fltyp == 'Large Audio File':

    # create a speech recognition object
    r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
#@st.cache
def get_large_audio_transcription(path):
    st.write(path)
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                st.write("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                st.write(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

if fltyp == 'Large Audio File':
    if __name__ == '__main__':
        import sys
        path = 'LongWelcome.wav'
        st.write("\nFull text:", get_large_audio_transcription(path))






