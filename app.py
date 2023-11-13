import streamlit as st
from streamlit_chat import message
import requests
from langchain.callbacks.base import BaseCallbackHandler

if "msg" not in st.session_state:
    st.session_state["msg"] = []

url = "http://localhost:8000/chatbot"


def chat_bot(text):
    user_turn = {"msg": text}
    msg = st.session_state["msg"]
    resp = requests.post(url, json=user_turn)
    assistant_turn = resp.json()

    st.session_state["msg"].append(user_turn)
    st.session_state["msg"].append(assistant_turn)



st.title("Hybrid Chatbot")

row1 = st.container()
row2 = st.container()


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token
        self.container.markdown(self.text)



input_text = st.chat_input("입력해주세요")
if input_text:
    chat_bot(text = input_text)


for i, msg_obj in enumerate(st.session_state["msg"]):
    msg = msg_obj["msg"]

    is_user = False
    if i % 2 == 0:
        is_user = True

    
    message(msg, is_user=is_user, key=f"chat_{i}")