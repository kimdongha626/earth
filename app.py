import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 페이지 설정
st.set_page_config(page_title="지진 위험도 분석 시스템", layout="centered")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #666;
        margin-bottom: 30px;
    }
    .risk-high {
        font-size: 28px;
        font-weight: bold;
        color: #e63946;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 타이틀 영역 ---
st.markdown('<div class="main-title">세계 지진 위험도 분석 시스템</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">위도와 경도를 입력하면 주변 지진 데이터를 기반으로 위험도를 분석합니다.</div>', unsafe_allow_html=True)

# --- 입력 필드 ---
col1, col2 = st.columns(2)
with col1:
    lat_input = st.number_input("위도 입력", value=37.56, step=0.01, format="%.2f")
with col2:
    lon_input = st.number_input("경도 입력", value=127.05, step=0.01, format="%.2f")

# --- 버튼 클릭 이벤트 처리 ---
# 버튼을 누르는 시점에만 입력된 위도/경도를 세션 상태에 고정합니다.
if st.button("위험도 분석"):
    st.session_state['analyzed'] = True
    st.session_state['target_lat'] = lat_input
    st.session_state['target_lon'] = lon_input

# --- 분석 결과 및 지도 시각화 ---
if st.session_state.get('analyzed', False):
    # 버튼 클릭 시점의 위도/경도 가져오기
    lat = st.session_state['target_lat']
    lon = st.session_state['target_lon']

    # 결과 메시지
    st.markdown('<div class="risk-high">예상 위험도: 높음 🔗</div>', unsafe_allow_html=True)

    # 1. 가상의 지진 데이터 생성 (지도 표시용)
    # 입력 위치 근처에 무작위 점들 생성
    np.random.seed(42)
    num_points = 50
    data = pd.DataFrame({
        'lat': lat + np.random.uniform(-10, 10, num_points),
        'lon': lon + np.random.uniform(-20, 20, num_points),
        'color': np.random.choice(['red', 'green', 'blue'], num_points)
    })

    # 2. Folium 지도 생성
    m = folium.Map(location=[lat, lon], zoom_start=4, control_scale=True)

    # 3. 데이터 마커 추가
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color=row['color'],
            fill=True,
            fill_color=row['color'],
            fill_opacity=0.7
        ).add_to(m)

    # 4. 현재 분석 위치 마커 (검은색 별 모양 아이콘)
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color='black', icon='star'),
        tooltip="분석 위치"
    ).add_to(m)

    # 5. 지도 표시 (값이 바뀔 때마다 동적으로 그려지도록 dynamic key 적용)
    st_folium(m, width=700, height=500, key=f"map_{lat}_{lon}")

else:
    # 초기 지도 (데이터 없이 기본 서울 위치 표시)
    m = folium.Map(location=[37.56, 127.05], zoom_start=4)
    st_folium(m, width=700, height=500, key="init_map")
