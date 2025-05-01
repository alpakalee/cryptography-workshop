# 2week/frequency_analysis.py

import streamlit as st
from collections import Counter
import re

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
    
    # 영어 알파벳 빈도 정보 표시
    st.write("### 영어 알파벳 빈도 (높은 순)")
    english_freq = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
    english_freq_percent = [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.0, 5.9, 4.3, 4.0, 2.8, 2.8, 2.4, 2.2, 2.0, 1.9, 1.5, 1.3, 1.0, 0.8, 0.8, 0.2, 0.2, 0.1, 0.1]
    
    freq_df = {"글자": list(english_freq), "빈도(%)": english_freq_percent}
    st.dataframe(freq_df, width=400)
    
    # 탭 생성
    tab1, tab2 = st.tabs(["빈도 분석 도구", "예제 분석"])
    
    with tab1:
        st.header("빈도 분석 도구")
        
        ciphertext = st.text_area("암호문을 입력하세요:", 
                                 """
                                 QSX KHDGC LPFRE ZFY OTNVU FWXP QSX JMBA VFI.
                                 D GFRQ CDCX QF UXGPAUQ QSDU NXUUMIX ZFP AFT.
                                 DZ AFT GMR PXMV QSDU, AFT SMWX UTGGXUUZTJJA
                                 VXGPAUQXV QSX NDRUQFR GSDTPGSDJ KTFQX.
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
            st.dataframe(result_data)
            
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
            
            st.write("""
            ### 참고:
            빈도 분석만으로는 완벽한 해독이 어려울 수 있습니다.
            실제로는 초기 매핑 후 문맥을 고려하여 수동으로 조정하는 과정이 필요합니다.
            """)
    
    with tab2:
        st.header("예제 분석")
        
        st.write("### 예제 1: 셜록 홈즈의 '춤추는 인형들'")
        
        holmes_cipher = """
        53‡‡†305))6*;4826)4‡.)4‡);806*;48†8¶60))85;;]8*;:‡*8†83(88)5*†;46(;88*96*?;8)*‡(;485);5*†2:*‡(;4956*2(5*—4)8¶8*;4069285);)6†8)4‡‡;1(‡9;48081;8:8‡1;48†85;4)485†528806*81(‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?;
        """
        
        st.code(holmes_cipher)
        
        st.write("""
        이 암호는 코난 도일의 "셜록 홈즈의 춤추는 인형들"에 등장하는 실제 암호입니다.
        이 소설에서 홈즈는 빈도 분석을 사용하여 이 암호가 단일 치환 암호임을 파악하고 해독합니다.
        
        홈즈의 해독 과정:
        1. 가장 자주 등장하는 기호가 'e'일 것이라 추정
        2. 단일 글자 단어는 'a'나 'I'일 것이라 추정
        3. 단어 마지막에 자주 등장하는 패턴에 주목
        4. 점진적으로 매핑을 확장하여 전체 해독
        """)
    
    # 코드 완성 문제
    st.write("---")
    st.header("코드 완성 문제")
    
    st.code("""
from collections import Counter
import re

def analyze_frequency(text):
    # 전처리: 알파벳만 추출하고 대문자로 변환
    text = re.sub(r'[^A-Za-z]', '', text).upper()
    
    # 여기에 코드를 작성하세요
    # Counter 클래스를 사용하여 각 문자의 등장 횟수를 계산합니다
    
    return []  # (문자, 빈도수) 튜플의 리스트를 반환하도록 수정하세요
    """, language="python")
    
    st.write("""
    ### 힌트:
    1. collections 모듈의 Counter 클래스를 사용하세요.
    2. Counter.most_common() 메서드는 빈도수 내림차순으로 정렬된 (요소, 빈도수) 튜플의 리스트를 반환합니다.
    """)
    
    answer = st.text_area("답안 작성:", height=150)
    if st.button("정답 확인"):
        correct_answer = """
freq_counter = Counter(text)
return freq_counter.most_common()
        """
        if "Counter(text)" in answer and "most_common()" in answer:
            st.success("정답입니다! 올바른 빈도 분석 코드를 작성했습니다.")
        else:
            st.error("틀렸습니다. Counter 클래스와 most_common() 메서드를 사용했는지 확인하세요.")

if __name__ == "__main__":
    frequency_analysis_app()