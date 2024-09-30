import streamlit as st
import os
import time
import telebot
from openai import OpenAI
from pypdf import PdfReader
from st_copy_to_clipboard import st_copy_to_clipboard

# Set up Telegram Bot
recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

# Retrieve the API keys from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=CLIENT_API_KEY)

st.set_page_config(page_title="Sherwood Analyst", page_icon=":desktop_computer:",)
st.write("**Sherwood Analyst**, your smart analyst")

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf','Enter free text'))

instruction = "Read the input below. Analyse the implications at the regional and international level."

if Option_Input == "Upload a pdf":
  uploaded_file = st.file_uploader("Upload a PDF to analyse:", type = "pdf")
  raw_text = ""
  if uploaded_file is not None:
    try:
      doc_reader = PdfReader(uploaded_file)
      with st.spinner("Extracting from PDF document..."):
        for i, page in enumerate(doc_reader.pages):
          text = page.extract_text()
          if text:
            raw_text = raw_text + text + "\n"
    except:
      st.error(" Error occurred when loading document", icon="🚨")
elif Option_Input == "Enter free text":
  raw_text = ""
  input_text = st.text_area("Enter the text you would like me to analyse and click **Let\'s Go! :desktop_computer:**")
  if st.button("Let\'s Go! :desktop_computer:"):
    raw_text = input_text + "\n..."

if raw_text.strip() != "":
  try:
    with st.spinner("Running AI Model..."):
      start = time.time()
      input = instruction + "\n\n" + raw_text
      response = client.chat.completions.create(model="o1-preview", 
                                                messages=[{"role": "user", "content": input}])
      output_text = response.choices[0].message.content
      end = time.time()

    with st.expander("Sherwood Analyst", expander = True):
      st.write(output_text)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
    st_copy_to_clipboard(output_text)
    
    bot.send_message(chat_id=recipient_user_id, text="Sherwood Analyst")
  except:
    st.error(" Error occurred when running model", icon="🚨")
