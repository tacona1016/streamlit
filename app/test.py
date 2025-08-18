import streamlit as st
import pandas as pd
import psycopg2
import yfinance as yf
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import warnings

# 모든 경고 무시
warnings.filterwarnings("ignore")
load_dotenv()

host = os.environ["SUPABASE_HOST"]
port = os.environ.get("SUPABASE_PORT", 5432)
db   = os.environ["SUPABASE_DB"]
user = os.environ["SUPABASE_USER"]
pw   = os.environ["SUPABASE_PASSWORD"]

url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
engine = create_engine(url, connect_args={"sslmode":"require"}, pool_pre_ping=True)

# 연결 테스트
with engine.begin() as conn:
    df_test = pd.read_sql("SELECT * FROM stock_addp", engine)
tickers = list(df_test.alias.unique())

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout = "wide",
    page_icon = "🍕",
    page_title = "tacona1016의 개인 대시보드"
)

with st.sidebar:
    st.write("Side bar test")
    st.write("tacona1016의 개인 차트")


st.write("몇가지 simple한 파생 parameter")

col1, col2, col3 = st.columns([2,1,1])
ticker = col1.selectbox('Name', options=tickers or ['금/은'])
start = col2.date_input('Start', value=pd.to_datetime('2022-01-01'))
end = col3.date_input('End', value=pd.to_datetime('today'))
start = pd.to_datetime(start)  # st_date: date | datetime
end   = pd.to_datetime(end)

df = df_test[(df_test.alias==ticker)&(df_test.date>=start)&(df_test.date<=end)]
st.line_chart(df.set_index('date')['value'])