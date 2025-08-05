import streamlit as st
import pandas as pd

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout = "wide",
    page_icon = "🍕",
    page_title = "tacona1016의 개인 대시보드"
)

with st.sidebar:
    st.write("Side bar test")
    st.write("tacona1016의 개인 차트")

