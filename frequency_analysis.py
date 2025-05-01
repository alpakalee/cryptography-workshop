# 2week/frequency_analysis.py

import streamlit as st
from collections import Counter
import re
import pandas as pd
import plotly.express as px
import numpy as np

def analyze_frequency(text):
    """
    텍스트의 문자 빈도를 분석하는 함수
    
    매개변수:
        text (str): 분석할 텍스트
        
    반환값:
        list: (문자, 출현 횟수) 튜플의 리스트 (빈도 내림차순)
    """
    # 전처리: 알파벳만 추출하고 대문자로 변환
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    
    # Counter 클래스를 사용하여 각 문자의 등장 횟수를 계산
    freq_counter = Counter(text)
    
    # 빈도수 내림차순으로 정렬
    return freq_counter.most_common()

def create_mapping_table(freq_data):
    """
    빈도 분석을 기반으로 암호문에서 평문으로의 매핑 테이블을 생성하는 함수
    
    매개변수:
        freq_data: (문자, 빈도수) 튜플의 리스트
        
    반환값:
        dict: 암호문 글자 -> 추정 평문 글자의 매핑 사전
    """
    # 영어 알파벳 빈도 (가장 빈번한 것부터 정렬)
    english_freq = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
    
    mapping = {}
    cipher_chars = [char for char, _ in freq_data]
    
    # 빈도 순서대로 영어 알파벳과 매핑
    for i, char in enumerate(cipher_chars):
        if i < len(english_freq):
            mapping[char] = english_freq[i]
    
    return mapping

def decrypt_with_mapping(ciphertext, mapping):
    """
    생성된 매핑 테이블을 사용하여 암호문을 복호화하는 함수
    
    매개변수:
        ciphertext (str): 암호문
        mapping (dict): 암호문 글자 -> 평문 글자 매핑
        
    반환값:
        str: 복호화된 텍스트
    """
    result = ""
    
    for char in ciphertext:
        if char.upper() in mapping and char.isupper():
            # 대문자인 경우
            result += mapping[char]
        elif char.upper() in mapping and char.islower():
            # 소문자인 경우
            result += mapping[char.upper()].lower()
        else:
            # 매핑이 없는 경우 그대로 추가
            result += char
    
    return result

def frequency_analysis_app():
    st.title("빈도 분석 기반 암호 해독")
    
    st.write("""
    ### 빈도 분석이란?
    빈도 분석은 암호문에서 각 문자의 출현 빈도를 분석하여 단일 치환 암호를 해독하는 기법입니다.
    영어에서는 E, T, A, O, I, N 등의 글자가 자주 등장하는데, 이러한 통계적 특성을 활용합니다.
    
    ### 단일 치환 암호란?
    단일 치환 암호는 평문의 각 글자를 다른 고정된 글자로 일관되게 대체하는 암호화 방식입니다.
    예를 들어, 모든 'A'는 'X'로, 모든 'B'는 'Y'로 치환하는 방식입니다.
    """)
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["빈도 분석 도구", "문자 빈도 시각화", "암호 해독 퍼즐"])
    
    with tab1:
        st.header("빈도 분석 도구")
        
        # 영어 알파벳 빈도 정보 표시
        st.write("### 영어 알파벳 빈도 (높은 순)")
        english_freq = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
        english_freq_percent = [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.0, 5.9, 4.3, 4.0, 2.8, 2.8, 2.4, 2.2, 2.0, 1.9, 1.5, 1.3, 1.0, 0.8, 0.8, 0.2, 0.2, 0.1, 0.1]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 막대 그래프로 시각화
            freq_df = pd.DataFrame({
                "글자": list(english_freq),
                "빈도(%)": english_freq_percent
            })
            fig = px.bar(freq_df, x="글자", y="빈도(%)", title="영어 알파벳 출현 빈도", 
                        color="빈도(%)", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            freq_df = {"글자": list(english_freq), "빈도(%)": english_freq_percent}
            st.dataframe(freq_df, width=400)
        
        ciphertext = st.text_area("암호문을 입력하세요:", 
                                """
                                QSX KHDGC LPFRE ZFY OTNVU FWXP QSX JMBA VFI.
                                D GFRQ CDCX QF UXGPAUQ QSDU NXUUMIX ZFP AFT.
                                DZ AFT GMR PXMV QSDU, AFT SMWX UTGGXUUZTJJA
                                VXGPAUQXV QSX NDRUQFR GSTPGSDJ KTFQX.
                                """, 
                                height=150)
        
        if st.button("빈도 분석 실행"):
            # 빈도 분석 수행
            freq_data = analyze_frequency(ciphertext)
            
            # 결과 표시
            st.write("### 문자 빈도 분석 결과:")
            
            total_chars = sum(count for _, count in freq_data)
            
            # 데이터프레임 형태로 표시
            result_data = {
                "문자": [char for char, _ in freq_data],
                "빈도수": [count for _, count in freq_data],
                "백분율(%)": [round((count / total_chars) * 100, 2) for _, count in freq_data]
            }
            
            result_df = pd.DataFrame(result_data)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # 빈도 분석 결과 시각화
                fig = px.bar(result_df, x="문자", y="빈도수", title="암호문 문자 빈도 분석",
                            color="빈도수", color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(result_df)
            
            # 매핑 테이블 생성
            mapping = create_mapping_table(freq_data)
            
            st.write("### 추정된 매핑 테이블:")
            mapping_data = {
                "암호문 글자": list(mapping.keys()),
                "추정 평문 글자": list(mapping.values())
            }
            st.dataframe(mapping_data, width=400)
            
            # 복호화 시도
            decrypted = decrypt_with_mapping(ciphertext, mapping)
            
            st.write("### 빈도 분석 기반 복호화 결과:")
            st.info(decrypted)
            
            # 매핑 조정 UI 추가
            st.write("### 매핑 수동 조정:")
            st.write("빈도 분석만으로는 완벽한 해독이 어려울 수 있습니다. 아래에서 문맥을 고려하여 매핑을 수동으로 조정해보세요.")
            
            col1, col2, col3 = st.columns(3)
            
            adjusted_mapping = dict(mapping)
            
            # 사용자 정의 매핑 입력 필드
            for i, (cipher_char, plain_char) in enumerate(mapping.items()):
                if i % 3 == 0:
                    with col1:
                        new_char = st.text_input(f"{cipher_char} →", plain_char, max_chars=1, key=f"char_{cipher_char}_1")
                        if new_char and new_char.isalpha():
                            adjusted_mapping[cipher_char] = new_char.upper()
                elif i % 3 == 1:
                    with col2:
                        new_char = st.text_input(f"{cipher_char} →", plain_char, max_chars=1, key=f"char_{cipher_char}_2")
                        if new_char and new_char.isalpha():
                            adjusted_mapping[cipher_char] = new_char.upper()
                else:
                    with col3:
                        new_char = st.text_input(f"{cipher_char} →", plain_char, max_chars=1, key=f"char_{cipher_char}_3")
                        if new_char and new_char.isalpha():
                            adjusted_mapping[cipher_char] = new_char.upper()
            
            if st.button("조정된 매핑으로 복호화"):
                adjusted_decrypted = decrypt_with_mapping(ciphertext, adjusted_mapping)
                st.write("### 조정된 복호화 결과:")
                st.success(adjusted_decrypted)
    
    with tab2:
        st.header("문자 빈도 시각화")
        
        st.write("""
        문자 빈도 분석은 암호 해독의 기본 도구입니다. 다양한 언어마다 서로 다른 문자 빈도 분포를 가지고 있습니다.
        아래 텍스트 입력 상자에 분석하고 싶은 텍스트를 붙여넣고 분석 버튼을 클릭해보세요.
        """)
        
        sample_text = st.text_area(
            "분석할 텍스트를 입력하세요:", 
            """
            가장 많은 사랑을 받는 셜록 홈즈의 모험들 중 암호 해독이 중요한 역할을 하는 이야기는
            '춤추는 인형들'입니다. 이 이야기에서 홈즈는 빈도 분석을 사용하여 특별한 암호를 해독하고
            범죄를 해결합니다. 단일 치환 암호와 빈도 분석의 중요성을 잘 보여주는 사례입니다.
            """, 
            height=150,
            key="vis_text"
        )
        
        if st.button("문자 빈도 분석", key="vis_button"):
            # 텍스트 전처리
            cleaned_text = re.sub(r'[^A-Za-z]', '', sample_text).upper()
            
            if cleaned_text:
                # 빈도 분석
                freq_counter = Counter(cleaned_text)
                freq_data = freq_counter.most_common()
                
                # 결과 데이터프레임
                freq_df = pd.DataFrame({
                    "문자": [char for char, _ in freq_data],
                    "빈도수": [count for _, count in freq_data]
                })
                
                # 모든 알파벳에 대한 빈도를 포함하도록 확장
                all_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                existing_letters = set(freq_df["문자"])
                missing_letters = all_letters - existing_letters
                
                # 누락된 문자 추가
                for letter in missing_letters:
                    freq_df = pd.concat([freq_df, pd.DataFrame({"문자": [letter], "빈도수": [0]})])
                
                # 문자 순서로 정렬
                freq_df = freq_df.sort_values("문자").reset_index(drop=True)
                
                # 일반적인 영어 빈도와 비교
                english_freq_dict = {letter: percent for letter, percent in zip(english_freq, english_freq_percent)}
                english_freq_df = pd.DataFrame({
                    "문자": list(english_freq_dict.keys()),
                    "일반 영어 빈도(%)": list(english_freq_dict.values())
                })
                
                # 알파벳 순으로 정렬
                english_freq_df = english_freq_df.sort_values("문자").reset_index(drop=True)
                
                # 두 데이터프레임 병합
                combined_df = pd.merge(freq_df, english_freq_df, on="문자")
                
                # 사용자 텍스트의 백분율 계산
                total = combined_df["빈도수"].sum()
                if total > 0:  # 0으로 나누기 방지
                    combined_df["분석 텍스트 빈도(%)"] = combined_df["빈도수"] / total * 100
                else:
                    combined_df["분석 텍스트 빈도(%)"] = 0
                
                # 그래프로 시각화
                fig = px.bar(
                    combined_df, 
                    x="문자", 
                    y=["분석 텍스트 빈도(%)", "일반 영어 빈도(%)"],
                    title="문자 빈도 비교: 분석 텍스트 vs 일반 영어",
                    barmode="group"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 표로도 표시
                st.dataframe(combined_df[["문자", "빈도수", "분석 텍스트 빈도(%)", "일반 영어 빈도(%)"]])
                
                # 분석 결과 해석
                st.write("### 분석 결과 해석")
                st.write("""
                위 그래프에서는 입력한 텍스트의 문자 빈도와 일반적인 영어 텍스트의 문자 빈도를 비교해 볼 수 있습니다.
                큰 차이가 있는 문자는 특별한 의미를 가질 수 있으며, 암호 해독 시 중요한 단서가 될 수 있습니다.
                """)
            else:
                st.error("분석할 영문 텍스트가 없습니다. 영문이 포함된 텍스트를 입력해주세요.")
    
    with tab3:
        st.header("암호 해독 퍼즐: 춤추는 인형들")
        
        st.write("""
        ### 춤추는 인형들의 비밀
        
        셜록 홈즈 시리즈 중 '춤추는 인형들'은 빈도 분석과 암호 해독의 중요성을 보여주는 명작입니다.
        이야기에서 힐튼 큐빗은 그의 아내가 이상한 춤추는 인형 그림을 받고 놀라는 것을 보게 됩니다.
        홈즈는 이 그림이 단일 치환 암호라는 것을 알아내고 빈도 분석을 통해 해독합니다.
        
        아래 예제를 통해 여러분도 홈즈처럼 암호를 해독해 보세요!
        """)
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Dancing_Men_cipher.svg/400px-Dancing_Men_cipher.svg.png", 
                caption="원작에 등장하는 춤추는 인형 암호")
        
        st.write("""
        ### 우리의 암호 퍼즐
        
        아래는 한국의 유명한 시인 '윤동주'의 시 '서시'의 일부를 단일 치환 암호로 암호화한 것입니다.
        빈도 분석을 활용하여 이 암호문을 해독해 보세요.
        """)
        
        # 한국 정서에 맞는 암호문 예제 (윤동주의 '서시' 일부를 단일 치환 암호화)
        korean_cipher = """
        HGBOGF CF KFG EYZZ CIH KYBK EHG DGRFYEM.
        Y RYPK KF ZYLG EYKIFNK HGDOGK
        YP KIG IGBLGPE KIBK UGIFZM NG.
        KIG EYPM, KIG UYOME, KIG EKBOE BPM BZZ KIG KIYPLE
        KIBK IBHH CF PBNG NG, BGEKIGKYX WFGKOC.
        """
        
        st.code(korean_cipher, language="text")
        
        st.write("""
        ### 힌트:
        1. 영어에서 가장 자주 등장하는 글자는 E, T, A, O, I, N입니다.
        2. 한 글자 단어는 보통 'A'나 'I'입니다.
        3. 가장 자주 등장하는 세 글자 단어는 'THE'입니다.
        4. 자주 등장하는 두 글자 단어로는 'OF', 'TO', 'IN', 'IS', 'IT' 등이 있습니다.
        """)
        
        # 퍼즐 해독 도구
        st.write("### 퍼즐 해독 도구")
        
        # 암호문 분석 수행
        if st.button("암호문 분석하기", key="puzzle_analyze"):
            # 빈도 분석
            puzzle_freq = analyze_frequency(korean_cipher)
            
            total_chars = sum(count for _, count in puzzle_freq)
            
            # 결과 시각화
            puzzle_data = {
                "문자": [char for char, _ in puzzle_freq],
                "빈도수": [count for _, count in puzzle_freq],
                "백분율(%)": [round((count / total_chars) * 100, 2) for _, count in puzzle_freq]
            }
            
            puzzle_df = pd.DataFrame(puzzle_data)
            
            # 그래프로 표시
            fig = px.bar(
                puzzle_df, 
                x="문자", 
                y="빈도수",
                title="암호문 빈도 분석",
                color="빈도수",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 자주 등장하는 패턴 분석
            st.write("### 자주 등장하는 패턴:")
            
            # 단어 추출
            words = re.findall(r'\b[A-Z]+\b', korean_cipher)
            word_freq = Counter(words)
            
            # 자주 등장하는 단어
            st.write("#### 자주 등장하는 단어:")
            common_words = word_freq.most_common(10)
            
            word_data = {
                "단어": [word for word, _ in common_words],
                "빈도수": [count for _, count in common_words]
            }
            st.dataframe(pd.DataFrame(word_data))
            
            # 단일 문자 단어 확인
            single_letters = [word for word in words if len(word) == 1]
            if single_letters:
                st.write(f"한 글자 단어: {', '.join(set(single_letters))}")
                st.write("(영어에서 한 글자 단어는 주로 'a'와 'I'입니다)")
            
            # 매핑 테이블 생성
            mapping = create_mapping_table(puzzle_freq)
            
            st.write("### 추정된 매핑 테이블:")
            mapping_data = {
                "암호문 글자": list(mapping.keys()),
                "추정 평문 글자": list(mapping.values())
            }
            st.dataframe(pd.DataFrame(mapping_data), width=400)
        
        # 사용자 매핑 입력 UI
        st.write("### 나만의 암호 해독:")
        st.write("위의 분석 결과를 바탕으로, 각 암호문 글자가 어떤 평문 글자에 해당하는지 직접 매핑해보세요.")
        
        # 알파벳 입력 필드 구성
        col1, col2, col3, col4 = st.columns(4)
        user_mapping = {}
        
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(alphabet):
            if i % 4 == 0:
                with col1:
                    mapped = st.text_input(f"{letter} →", "", max_chars=1, key=f"map_{letter}_1")
                    if mapped and mapped.isalpha():
                        user_mapping[letter] = mapped.upper()
            elif i % 4 == 1:
                with col2:
                    mapped = st.text_input(f"{letter} →", "", max_chars=1, key=f"map_{letter}_2")
                    if mapped and mapped.isalpha():
                        user_mapping[letter] = mapped.upper()
            elif i % 4 == 2:
                with col3:
                    mapped = st.text_input(f"{letter} →", "", max_chars=1, key=f"map_{letter}_3")
                    if mapped and mapped.isalpha():
                        user_mapping[letter] = mapped.upper()
            else:
                with col4:
                    mapped = st.text_input(f"{letter} →", "", max_chars=1, key=f"map_{letter}_4")
                    if mapped and mapped.isalpha():
                        user_mapping[letter] = mapped.upper()
        
        if st.button("내 매핑으로 해독"):
            # 사용자 매핑으로 해독
            if user_mapping:
                user_decrypted = decrypt_with_mapping(korean_cipher, user_mapping)
                st.write("### 해독 결과:")
                st.info(user_decrypted)
                
                # 정답 확인
                correct_answer = """
                WISHING MY NAME NOT HURT ANYONE.
                I WANT TO LIVE WITHOUT REGRET
                IN THE HEAVENS THAT BEHOLD ME.
                THE WIND, THE BIRDS, THE STARS AND ALL THE THINGS
                THAT HAVE MY NAME ME, AESTHETIC POETRY.
                """
                
                # 정답과 비교 (대소문자 무시하고 공백만 비교)
                user_clean = re.sub(r'\s+', '', user_decrypted.upper())
                answer_clean = re.sub(r'\s+', '', correct_answer.upper())
                
                similarity = sum(1 for a, b in zip(user_clean, answer_clean) if a == b) / max(len(user_clean), len(answer_clean))
                
                if similarity > 0.8:
                    st.success("축하합니다! 암호를 성공적으로 해독했습니다!")
                    st.write("이 암호문은 윤동주의 '서시' 일부를 영어로 번역한 것입니다.")
                    st.write("""
                    원문:
                    '하늘을 우러러 한 점 부끄럼이 없기를,
                    잎새에 이는 바람에도 나는 괴로워했다.
                    별을 노래하는 마음으로 모든 죽어가는 것을 사랑해야지'
                    """)
                elif similarity > 0.5:
                    st.warning("암호 해독이 진행 중입니다. 좋은 진전을 보이고 있어요!")
                else:
                    st.error("아직 정확한 해독이 아닙니다. 다시 시도해보세요.")
            else:
                st.error("매핑을 입력해주세요.")

if __name__ == "__main__":
    frequency_analysis_app()