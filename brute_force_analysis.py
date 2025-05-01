# 2week/brute_force_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math

def calculate_keyspace(length, charset_size):
    """
    주어진 길이와 문자셋 크기로 가능한 키스페이스를 계산
    
    매개변수:
        length (int): 비밀번호 길이
        charset_size (int): 문자셋 크기
    
    반환값:
        int: 가능한 키스페이스 크기
    """
    return charset_size ** length

def calculate_time(keyspace, attempts_per_second):
    """
    키스페이스와 초당 시도 횟수로 브루트포스 소요 시간 계산
    
    매개변수:
        keyspace (int): 키스페이스 크기
        attempts_per_second (int): 초당 시도 횟수
    
    반환값:
        float: 소요 시간(초)
    """
    return keyspace / attempts_per_second

def time_to_human_readable(seconds):
    """
    초를 사람이 읽기 쉬운 형태로 변환
    
    매개변수:
        seconds (float): 초 단위 시간
    
    반환값:
        str: 사람이 읽기 쉬운 형태의 시간
    """
    if seconds < 60:
        return f"{seconds:.2f} 초"
    elif seconds < 3600:
        return f"{seconds/60:.2f} 분"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} 시간"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} 일"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.2f} 년"
    else:
        return f"{seconds/31536000:.2e} 년"

def brute_force_analysis_app():
    st.title("키스페이스 크기와 브루트포스 시간 분석")
    
    st.write("""
    ### 암호 복잡성과 해독 시간의 관계
    비밀번호 길이와 사용되는 문자 종류에 따라 키스페이스(가능한 조합의 수)가 달라지고, 
    이에 따라 브루트포스 공격(모든 가능한 경우를 시도하는 방식)에 필요한 시간도 크게 변화합니다.
    
    이 도구를 통해 다양한 조건에서 비밀번호를 해독하는 데 필요한 시간을 시뮬레이션해볼 수 있습니다.
    """)
    
    # 사이드바에 입력 설정
    st.sidebar.header("브루트포스 설정")
    
    # 비밀번호 길이 설정
    min_length = st.sidebar.number_input("최소 비밀번호 길이", min_value=1, max_value=16, value=4)
    max_length = st.sidebar.number_input("최대 비밀번호 길이", min_value=min_length, max_value=20, value=12)
    
    # 문자셋 설정
    st.sidebar.subheader("사용할 문자셋 선택:")
    use_lowercase = st.sidebar.checkbox("소문자 (a-z, 26개)", value=True)
    use_uppercase = st.sidebar.checkbox("대문자 (A-Z, 26개)", value=False)
    use_digits = st.sidebar.checkbox("숫자 (0-9, 10개)", value=False)
    use_special = st.sidebar.checkbox("특수문자 (~!@#$%^&*()_+, 32개)", value=False)
    
    # 문자셋 크기 계산
    charset_size = 0
    if use_lowercase:
        charset_size += 26
    if use_uppercase:
        charset_size += 26
    if use_digits:
        charset_size += 10
    if use_special:
        charset_size += 32
    
    if charset_size == 0:
        st.error("최소한 하나의 문자셋을 선택해야 합니다.")
        charset_size = 26  # 기본값: 소문자만
    
    # 하드웨어 설정
    st.sidebar.subheader("하드웨어 설정:")
    hardware_option = st.sidebar.selectbox(
        "계산 장치 선택:",
        ["일반 PC", "고성능 PC", "GPU 가속", "슈퍼컴퓨터"]
    )
    
    # 하드웨어별 초당 시도 횟수 설정
    attempts_map = {
        "일반 PC": 1_000_000,              # 백만 시도/초
        "고성능 PC": 10_000_000,           # 천만 시도/초
        "GPU 가속": 1_000_000_000,         # 10억 시도/초
        "슈퍼컴퓨터": 100_000_000_000      # 1천억 시도/초
    }
    
    attempts_per_second = attempts_map[hardware_option]
    
    # 사용자 정의 시도 횟수
    custom_attempts = st.sidebar.checkbox("사용자 정의 시도 횟수 사용")
    if custom_attempts:
        attempts_per_second = st.sidebar.number_input(
            "초당 시도 횟수 입력", 
            min_value=1, 
            max_value=10**15, 
            value=attempts_per_second,
            format="%e"
        )
    
    # 키스페이스 및 시간 계산
    lengths = list(range(min_length, max_length + 1))
    keyspaces = [calculate_keyspace(length, charset_size) for length in lengths]
    times = [calculate_time(keyspace, attempts_per_second) for keyspace in keyspaces]
    
    # 데이터프레임 생성 - int64로 변환하여 PyArrow 오류 방지
    data = pd.DataFrame({
        "비밀번호 길이": lengths,
        "키스페이스 크기": [int(k) if k < 9223372036854775807 else float(k) for k in keyspaces],
        "소요 시간(초)": times,
        "소요 시간(사람 읽기용)": [time_to_human_readable(t) for t in times]
    })
    
    # 메인 화면에 결과 표시
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("브루트포스 시간 분석 결과")
        
        # 문자셋 정보 표시
        charset_info = ""
        if use_lowercase:
            charset_info += "소문자 (a-z) "
        if use_uppercase:
            charset_info += "대문자 (A-Z) "
        if use_digits:
            charset_info += "숫자 (0-9) "
        if use_special:
            charset_info += "특수문자 "
        
        st.write(f"**선택한 문자셋**: {charset_info}")
        st.write(f"**문자셋 크기**: {charset_size}개 문자")
        st.write(f"**계산 속도**: 초당 {attempts_per_second:,} 시도")
        
        # 그래프 그리기
        chart_type = st.selectbox("그래프 종류 선택:", ["로그 스케일", "선형 스케일"])
        
        if chart_type == "로그 스케일":
            fig = px.line(
                data, 
                x="비밀번호 길이", 
                y="소요 시간(초)", 
                log_y=True,
                labels={"비밀번호 길이": "비밀번호 길이", "소요 시간(초)": "소요 시간(초, 로그 스케일)"},
                title=f"비밀번호 길이에 따른 브루트포스 시간 (문자셋: {charset_size}개)"
            )
        else:
            fig = px.line(
                data, 
                x="비밀번호 길이", 
                y="소요 시간(초)",
                labels={"비밀번호 길이": "비밀번호 길이", "소요 시간(초)": "소요 시간(초)"},
                title=f"비밀번호 길이에 따른 브루트포스 시간 (문자셋: {charset_size}개)"
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 키스페이스 그래프도 추가
        fig2 = px.line(
            data, 
            x="비밀번호 길이", 
            y="키스페이스 크기",
            log_y=True,
            labels={"비밀번호 길이": "비밀번호 길이", "키스페이스 크기": "키스페이스 크기 (로그 스케일)"},
            title=f"비밀번호 길이에 따른 키스페이스 크기 (문자셋: {charset_size}개)"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("데이터 테이블")
        # 각 길이별 키스페이스와 브루트포스 시간 - 표시할 데이터만 선택
        display_data = pd.DataFrame({
            "비밀번호 길이": data["비밀번호 길이"],
            "키스페이스 크기": [f"{k:,.0f}" if isinstance(k, (int, float)) and k < 1e12 else f"{k:.2e}" for k in data["키스페이스 크기"]],
            "소요 시간": data["소요 시간(사람 읽기용)"]
        })
        st.dataframe(display_data)
    
    # 키스페이스와 시간의 관계 설명
    st.write("""
    ### 비밀번호 복잡도와 브루트포스의 관계
    
    **키스페이스란?**
    키스페이스는 가능한 모든 비밀번호의 조합 수입니다. 비밀번호 길이와 사용 가능한 문자셋에 직접적인 영향을 받습니다.
    
    **계산 방법:**
    - 키스페이스 = (문자셋 크기) ^ (비밀번호 길이)
    - 예: 소문자만 사용하는 4자리 비밀번호 → 26^4 = 456,976개
    - 예: 소문자+대문자+숫자를 사용하는 8자리 비밀번호 → 62^8 = 218,340,105,584,896개
    
    **브루트포스 공격 시간의 증가:**
    그래프에서 볼 수 있듯이, 비밀번호 길이나 문자셋이 증가할수록 브루트포스 시간은 기하급수적으로 증가합니다.
    이것이 복잡한 비밀번호를 사용해야 하는 이유입니다.
    
    **보안 권장사항:**
    - 최소 8자 이상의 비밀번호 사용
    - 문자셋을 다양하게 사용 (대소문자, 숫자, 특수문자 조합)
    - 정기적으로 비밀번호 변경
    """)
    
    # 비밀번호 강도를 시각적으로 보여주는 섹션
    st.subheader("비밀번호 강도 테스트")
    test_password = st.text_input("비밀번호 입력:", type="password")
    
    if test_password and st.button("분석"):
        # 비밀번호 강도 계산
        length = len(test_password)
        
        has_lower = any(c.islower() for c in test_password)
        has_upper = any(c.isupper() for c in test_password)
        has_digit = any(c.isdigit() for c in test_password)
        has_special = any(not c.isalnum() for c in test_password)
        
        charset_size_test = 0
        if has_lower:
            charset_size_test += 26
        if has_upper:
            charset_size_test += 26
        if has_digit:
            charset_size_test += 10
        if has_special:
            charset_size_test += 32
        
        keyspace_test = calculate_keyspace(length, charset_size_test)
        
        # 강도 분석 및 표시
        st.write(f"**비밀번호 길이**: {length}자리")
        st.write(f"**사용된 문자셋**: {charset_size_test}개 문자")
        st.write(f"**키스페이스 크기**: {keyspace_test:,}")
        
        # GPU 기준 브루트포스 시간
        gpu_time = calculate_time(keyspace_test, attempts_map["GPU 가속"])
        gpu_readable = time_to_human_readable(gpu_time)
        
        st.write(f"**GPU 가속 브루트포스 예상 시간**: {gpu_readable}")
        
        # 강도 평가
        if length < 8:
            st.error("위험: 비밀번호가 너무 짧습니다.")
        elif charset_size_test < 36:
            st.warning("주의: 더 다양한 문자를 사용하는 것이 좋습니다.")
        elif gpu_time < 86400:  # 1일 미만
            st.warning("주의: GPU로 하루 안에 해독 가능합니다.")
        elif gpu_time < 31536000:  # 1년 미만
            st.info("양호: GPU로 1년 이내에 해독 가능하지만 일반적으로 안전합니다.")
        else:
            st.success("안전: 브루트포스 공격으로 해독하기 매우 어렵습니다.")

if __name__ == "__main__":
    brute_force_analysis_app()