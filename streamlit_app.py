# 2week/streamlit_app.py

import streamlit as st

# 각 실습 모듈 가져오기
from caesar_cipher import caesar_cipher_app
from rot13_cipher import rot13_app
from frequency_analysis import frequency_analysis_app

def main():
    st.sidebar.title("암호학 실습")
    st.sidebar.write("2주차: 브루트 포스 & 빈도 분석")
    
    # 네비게이션
    app_mode = st.sidebar.radio(
        "실습을 선택하세요:",
        ["홈", "시저 암호 브루트 포스", "ROT13 암호", "빈도 분석 기반 암호 해독"]
    )
    
    # 홈 페이지
    if app_mode == "홈":
        st.title("암호학 실습: 브루트 포스 & 빈도 분석")
        
        st.write("""
        ### 환영합니다!
        이 웹 애플리케이션은 암호학의 기본 개념과 암호 해독 기법을 실습할 수 있는 플랫폼입니다.
        
        왼쪽 사이드바에서 원하는 실습을 선택하여 시작하세요.
        
        ### 제공되는 실습:
        1. **시저 암호 브루트 포스**: 시저 암호에 대한 무차별 대입 공격을 실습합니다.
        2. **ROT13 암호**: 시저 암호의 특별한 경우인 ROT13을 실습합니다.
        3. **빈도 분석 기반 암호 해독**: 문자 빈도 분석을 통한 단일 치환 암호 해독을 실습합니다.
        
        각 실습에는 이론 설명, 실습 도구, 그리고 코드 완성 문제가 포함되어 있습니다.
        """)
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Caesar_cipher_left_shift_of_3.svg/1200px-Caesar_cipher_left_shift_of_3.svg.png", 
                caption="시저 암호 시프트 다이어그램")
        
        st.write("""
        ### 학습 목표:
        - 브루트 포스 공격과 빈도 분석의 개념과 원리를 이해합니다.
        - Python을 사용하여 간단한 암호화 및 해독 알고리즘을 구현합니다.
        - 각 암호 기법의 강점과 취약점을 분석합니다.
        """)
    
    # 시저 암호 브루트 포스 앱
    elif app_mode == "시저 암호 브루트 포스":
        caesar_cipher_app()
    
    # ROT13 암호 앱
    elif app_mode == "ROT13 암호":
        rot13_app()
    
    # 빈도 분석 기반 암호 해독 앱
    elif app_mode == "빈도 분석 기반 암호 해독":
        frequency_analysis_app()

if __name__ == "__main__":
    main()