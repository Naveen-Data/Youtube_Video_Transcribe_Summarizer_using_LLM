import os 
import streamlit as st
from dotenv import load_dotenv

import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt_text =   """
                You are a Youtube video summarizer. You will be taking the video transcipt text as input
                and summarizing the entire video and 
                providing a brief summary of the video in points in 250 words.
                Transcipt text is as follows and please provide the summary of the text by following above instructions.: 
                """
def generate_gemini_content(transcript_text,prompt_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt_text+transcript_text)
    return response.text


def extract_trancript_text(video_url):
    try:
        video_id = video_url.split('=')[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        print(transcript_text)
        transcript = ' '
        for i in transcript_text:
            transcript = transcript + i['text']
        return transcript
    except Exception as e:
        return f"Error in extracting the transcript text: {e}"
    

st.title("Youtube Video Summarizer")
st.write("This app will summarize the entire video and provide a brief summary of the video in points in 250 words.")
video_url = st.text_input("Enter the Youtube Video URL: ")

if video_url:
    video_id = video_url.split('=')[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize"):
    transcript_text = extract_trancript_text(video_url)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt_text)
        st.markdown(' ## Detailed Summary')
        st.write(summary)