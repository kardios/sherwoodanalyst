import streamlit as st
import os
import time
import telebot
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import openai
from st_copy_to_clipboard import st_copy_to_clipboard

# Set up Telegram Bot
recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

# Retrieve the API keys from the environment variables
CLIENT_API_KEY = os.environ["OPENAI_API_KEY"]
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]

openai.api_key = CLIENT_API_KEY
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
    response = openai.chat.completions.create(model="o1-mini", messages=[{"role": "user", "content": input}])
    o1_mini_output = response.choices[0].message.content
    end = time.time()
    with st.expander("o1-mini output"):
      st.markdown(o1_mini_output)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(o1_mini_output)
    st.snow()

    start = time.time()
    input = research_topic
    response = openai.chat.completions.create(model="gpt-4o-2024-11-20", messages=[{"role": "user", "content": input}])
    gpt4o_output = response.choices[0].message.content
    end = time.time()
    with st.expander("gpt-4o output"):
      st.markdown(gpt4o_output)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(gpt4o_output)
    st.snow()

    start = time.time()
    input = "Read the answers contained in the <answer_1> and <answer_2> tags. Synthesize a new answer that integrates both answers. Try to maintain the content, especially the main ideas and key details in both answers. Present your output as a series of paragraphs, without headings.\n\n"
    input = input + "<answer_1>\n\n" + o1_mini_output + "\n\n</answer_1>\n\n"
    input = input + "<answer_2>\n\n" + gpt4o_output + "\n\n</answer_2>\n\n"
    anthropic.messages.create(model = "claude-3-5-sonnet-20241022", max_tokens = 4096, temperature = 0, system= "", messages=[{"role": "user", "content": input}])
    anthropic_output = message.content[0].text
    end = time.time()
    with st.expander("Claude 3.5 Sonnet output"):
      st.markdown(anthropic_output)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(anthropic_output)
    st.snow()

    start = time.time()
    input = "Check the the report below and highlight any inaccuracies or biases:\n\n" + anthropic_output
    gemini = genai.GenerativeModel("gemini-1.5-pro-002")
    response = gemini.generate_content(input, safety_settings = safety_settings, generation_config = generation_config, tools = "google_search_retrieval")
    verified_result = response.text
    end = time.time()
    with st.expander("Verification result"):
      st.markdown(verified_result)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(verified_result)
    st.snow()
    
