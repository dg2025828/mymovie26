import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
    최근 1년간 박스오피스 10위권에 든 영화 가운데, 이 기간에 개봉한 216편의 데이터를 살펴봅니다.
    """
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# ------------------------------------------------------------
# 데이터 불러오기 및 전처리
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자(YYYYMMDD) -> 날짜형
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르: 세로막대(|) 기호로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

st.divider()

# ------------------------------------------------------------
# 그래프 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)
genre_counts.columns = ["genre", "count"]

fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_donut.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_donut.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()
