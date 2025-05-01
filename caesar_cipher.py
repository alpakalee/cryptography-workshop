# 2week/caesar_cipher.py

import streamlit as st

def caesar_encrypt(text, shift):
    """
    시저 암호로 텍스트를 암호화하는 함수
    
    매개변수:
        text (str): 암호화할 원본 텍스트
        shift (int): 시프트 값 (1-25)
    
    반환값:
        str: 암호화된 텍스트
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # 대문자인 경우
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            # 소문자인 경우
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # 알파벳이 아닌 경우 그대로 추가
            result += char
    
    return result

def caesar_decrypt(ciphertext, shift):
    """
    시저 암호로 암호화된 텍스트를 복호화하는 함수
    
    매개변수:
        ciphertext (str): 복호화할 암호문
        shift (int): 시프트 값 (1-25)
    
    반환값:
        str: 복호화된 원본 텍스트
    """
    # 복호화는 암호화의 반대 방향으로 시프트하는 것과 같음
    return caesar_encrypt(ciphertext, 26 - shift)

def brute_force_caesar(ciphertext):
    """
    시저 암호로 암호화된 텍스트에 브루트 포스 공격을 수행하는 함수
    가능한 모든 시프트 값(1-25)에 대해 복호화를 시도합니다.
    
    매개변수:
        ciphertext (str): 복호화할 암호문
    
    반환값:
        list: (시프트 값, 복호화된 텍스트) 튜플의 리스트
    """
    results = []
    
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        results.append((shift, decrypted))
    
    return results

def caesar_cipher_app():
    st.title("시저 암호 브루트 포스 공격")
    
    st.write("""
    ### 시저 암호란?
    시저 암호는 각 글자를 알파벳 상에서 일정한 수만큼 이동시키는 암호화 방식입니다.
    예를 들어, 시프트 값이 3이면 'A'는 'D'로, 'B'는 'E'로 암호화됩니다.
    
    ### 브루트 포스(무차별 대입) 공격이란?
    가능한 모든 키(시저 암호의 경우 시프트 값 1-25)를 시도하여 원문을 찾아내는 방법입니다.
    """)
    
    # 탭 생성
    tab1, tab2 = st.tabs(["브루트 포스 공격", "암호화/복호화"])
    
    with tab1:
        st.header("브루트 포스 공격")
        ciphertext = st.text_area("암호문을 입력하세요:", "DWWDFN DW GDZQ", height=100)
        
        if st.button("브루트 포스 공격 실행"):
            results = brute_force_caesar(ciphertext)
            
            st.write("### 모든 가능한 시프트 값에 대한 결과:")
            for shift, decrypted in results:
                st.write(f"시프트 {shift}: {decrypted}")
    
    with tab2:
        st.header("암호화/복호화")
        
        mode = st.radio("모드 선택:", ["암호화", "복호화"])
        
        text = st.text_area("텍스트 입력:", "ATTACK AT DAWN" if mode == "암호화" else "DWWDFN DW GDZQ", height=100)
        shift = st.slider("시프트 값 (1-25):", 1, 25, 3)
        
        if st.button("실행"):
            if mode == "암호화":
                result = caesar_encrypt(text, shift)
                st.success(f"암호화 결과: {result}")
            else:
                result = caesar_decrypt(text, shift)
                st.success(f"복호화 결과: {result}")

    # 코드 완성 문제
    st.write("---")
    st.header("코드 완성 문제")
    
    st.code("""
def caesar_encrypt(text, shift):
    result = ""
    
    for char in text:
        if char.isalpha():
            # 대문자인 경우
            if char.isupper():
                # 여기에 코드를 작성하세요
                pass
            # 소문자인 경우
            else:
                # 여기에 코드를 작성하세요
                pass
        else:
            # 알파벳이 아닌 경우 그대로 추가
            result += char
    
    return result
    """, language="python")
    
    st.write("""
    ### 힌트:
    1. 알파벳을 시프트 값만큼 이동시키려면 ASCII 값을 활용하세요.
    2. ord() 함수를 사용하여 문자의 ASCII 값을 얻고, chr() 함수를 사용하여 ASCII 값을 문자로 변환할 수 있습니다.
    3. 알파벳의 범위를 벗어나지 않도록 모듈로 연산(%)을 사용하세요.
    """)
    
    answer = st.text_area("답안 작성:", height=150)
    if st.button("정답 확인"):
        correct_answer = """
result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        """
        if correct_answer.strip() in answer.strip():
            st.success("정답입니다! 올바른 암호화 코드를 작성했습니다.")
        else:
            st.error("틀렸습니다. 다시 시도해보세요.")

if __name__ == "__main__":
    caesar_cipher_app()