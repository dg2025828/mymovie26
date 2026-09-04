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

# ------------------------------------------------------------
# 그래프 2. 장르 안에 영화 - 트리맵 (칸 크기: 총 관객)
# ------------------------------------------------------------
st.header("2. 장르별 영화 트리맵 (칸 크기: 총 관객)")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 그래프 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3. 총 관객수 분포")

N_BINS = 20

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=N_BINS,
)
fig_hist.update_traces(
    hovertemplate="관객 구간: %{x}<br>영화 수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객 수(명)",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_hist, use_container_width=True)

# 대부분의 영화가 몰려 있는 구간 계산
bin_edges = pd.cut(df["total_audi"], bins=N_BINS)
most_common_bin = bin_edges.value_counts().idxmax()
bin_movie_count = bin_edges.value_counts().max()

# 가장 관객이 많은 영화 계산
top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"**이 그래프로 알 수 있는 것:** 대부분의 영화는 총 관객 "
    f"**{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명** 구간에 "
    f"**{bin_movie_count}편**이 몰려 있으며, 가장 관객이 많은 영화는 "
    f"**'{top_movie_row['movieNm']}'**로 총 **{top_movie_row['total_audi']:,}명**을 동원했다."
)

st.divider()

# ------------------------------------------------------------
# 그래프 4. 개봉일 스크린수 vs 총 관객 - 산점도 (색: 장르)
# ------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    custom_data=["movieNm"],
)
fig_scatter.update_traces(
    hovertemplate="영화명: %{customdata[0]}<br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수(개)",
    yaxis_title="총 관객 수(명)",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()
