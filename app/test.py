import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import yfinance as yf
import altair as alt
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
    st.write("윤석현의 개인 차트")
    st.write("tacona1016@gmail.com")


st.write("## 🪐Financial KPI trend")

col1, col2, col3 = st.columns([2,1,1])
ticker = col1.selectbox('Name', options=tickers or ['금/은'])
start = col2.date_input('Start', value=pd.to_datetime('2022-01-01'))
end = col3.date_input('End', value=pd.to_datetime('today'))
start = pd.to_datetime(start)  # st_date: date | datetime
end   = pd.to_datetime(end)

df = df_test[(df_test.alias==ticker)&(df_test.date>=start)&(df_test.date<=end)]

# 120일 이동평균 및 표준편차 계산
window = 120
df["ma120"] = df["value"].rolling(window).mean()
df["std120"] = df["value"].rolling(window).std()

# 상단/하단 밴드
df["upper"] = df["ma120"] + 2 * df["std120"]
df["lower"] = df["ma120"] - 2 * df["std120"]

y_min = df.value.min()
y_max = df.value.max()

if 'monthly' in ticker:
    dates = pd.date_range(start=start, end=end)
    hline = pd.DataFrame({"date": dates, "line": [0.0] * len(dates)})
    trend_chart = alt.Chart(df).mark_line(color="white").encode(x="date:T", y=alt.Y("value:Q", scale=alt.Scale(domain=[y_min, y_max])))
    hline_chart = alt.Chart(hline).mark_line(color="red").encode(x="date:T", y=alt.Y("line:Q", scale=alt.Scale(domain=[y_min, y_max])))
    st.altair_chart(trend_chart + hline_chart, use_container_width=True)
else :
    trend_chart = alt.Chart(df).mark_line(color="white").encode(x="date:T", y=alt.Y("value:Q", scale=alt.Scale(domain=[y_min, y_max])))
    ma_line = alt.Chart(df).mark_line(color="red").encode(x="date:T", y=alt.Y("ma120:Q", scale=alt.Scale(domain=[y_min, y_max])))
    upper_line = alt.Chart(df).mark_line(color="orange").encode(x="date:T", y=alt.Y("upper:Q", scale=alt.Scale(domain=[y_min, y_max])))
    lower_line = alt.Chart(df).mark_line(color="orange").encode(x="date:T", y=alt.Y("lower:Q", scale=alt.Scale(domain=[y_min, y_max])))
    st.altair_chart(trend_chart + ma_line + upper_line + lower_line, use_container_width=True)