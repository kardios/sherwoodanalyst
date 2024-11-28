import streamlit as st
import os
import time
import telebot
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI
from st_copy_to_clipboard import st_copy_to_clipboard

# Set up Telegram Bot
recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

# Retrieve the API keys from the environment variables
CLIENT_API_KEY = os.environ["OPENAI_API_KEY"]
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]

client = OpenAI(api_key=CLIENT_API_KEY)
anthropic = Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

safety_settings = {
  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config = genai.GenerationConfig(
  candidate_count = 1,
  temperature = 0,
)

st.set_page_config(page_title="Sherwood Analyst", page_icon=":desktop_computer:",)
st.write("**Sherwood Analyst**, your smart analyst")

research_topic = st.text_input("What is my research topic?", "Analyse the implications of Vietnam\'s Doi Moi reforms")

if st.button("Let\'s Go! :rocket:") and research_topic.strip()!="":
  
  with st.spinner("Running AI Model..."):

    start = time.time()
    input = research_topic
    response = client.chat.completions.create(model="o1-preview", messages=[{"role": "user", "content": input}])
    o1_preview_raw = response.choices[0].message.content
    end = time.time()
    with st.expander("Raw o1-preview output"):
      st.markdown(o1_preview_raw)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(o1_preview_raw)
    st.snow()

    start = time.time()
    input = "Rewrite the answer below into a series of paragraphs, without headings:\n\n" + research_topic
    response = client.chat.completions.create(model="gpt-4o-2024-11-20", messages=[{"role": "user", "content": input}])
    rewrite_raw = response.choices[0].message.content
    end = time.time()
    with st.expander("Raw gpt-4o rewritten"):
      st.markdown(rewrite_raw)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(rewrite_raw)
    st.snow()

    start = time.time()
    input = "Research facts, trends and statistics relevant to the topic:\n\n" + research_topic
    gemini = genai.GenerativeModel("gemini-1.5-pro-002")
    response = gemini.generate_content(input, safety_settings = safety_settings, generation_config = generation_config, tools = "google_search_retrieval")
    research_raw = response.text
    with st.expander("Raw research result"):
      st.markdown(research_raw)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(research_raw)
    st.snow()

    start = time.time()
    input = "Update <answer> with <research>:\n\n"
    input = input + "<answer>\n\n" + rewrite_raw + "\n\n</answer>\n\n"
    input = input + "<research>\n\n" + research_raw + "\n\n</research>\n\n"
    response = client.chat.completions.create(model="gpt-4o-2024-11-20", messages=[{"role": "user", "content": input}])
    updated_answer = response.choices[0].message.content
    end = time.time()
    with st.expander("Updated answer"):
      st.markdown(updated_answer)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(updated_answer)
    st.snow()
