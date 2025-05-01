# 2week/rot13_cipher.py

import streamlit as st

def rot13(text):
    """
    ROT13 암호화/복호화 함수 (동일 함수로 양방향 변환 가능)
    
    매개변수:
        text (str): 암호화 또는 복호화할 텍스트
    
    반환값:
        str: ROT13으로 변환된 텍스트
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # 대문자인 경우
            if char.isupper():
                result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
            # 소문자인 경우
            else:
                result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        else:
            # 알파벳이 아닌 경우 그대로 추가
            result += char
    
    return result

def rot13_app():
    st.title("ROT13 암호")
    
    st.write("""
    ### ROT13이란?
    ROT13은 시저 암호의 특별한 경우로, 알파벳을 13글자씩 시프트하는 간단한 암호화 방식입니다.
    
    특별한 점:
    - 알파벳이 26글자이므로, 13글자 시프트하면 정확히 반대편 글자가 됩니다.
    - 암호화와 복호화가 동일한 연산입니다 (즉, 암호문에 다시 ROT13을 적용하면 원문이 됩니다).
    - 인터넷 포럼에서 스포일러를 숨기는 등의 용도로 사용됩니다.
    """)
    
    # 탭 생성
    tab1, tab2 = st.tabs(["ROT13 변환", "예제 테스트"])
    
    with tab1:
        st.header("ROT13 변환")
        text = st.text_area("텍스트 입력:", "Hello, World!", height=100)
        
        if st.button("ROT13 변환 실행"):
            result = rot13(text)
            st.success(f"변환 결과: {result}")
            
            # 다시 변환하면 원문으로 돌아옴을 보여줌
            st.info(f"다시 변환 결과 (원문): {rot13(result)}")
    
    with tab2:
        st.header("예제 테스트")
        
        examples = [
            "Hello, World!",
            "The quick brown fox jumps over the lazy dog.",
            "ROT13 is a simple letter substitution cipher.",
            "Cryptography is fun!"
        ]
        
        for example in examples:
            converted = rot13(example)
            st.write(f"**원본**: {example}")
            st.write(f"**ROT13 변환**: {converted}")
            st.write(f"**다시 변환 (원문)**: {rot13(converted)}")
            st.write("---")
    
    # 코드 완성 문제
    st.write("---")
    st.header("코드 완성 문제")
    
    st.code("""
def rot13(text):
    result = ""
    
    for char in text:
        if char.isalpha():
            # 여기에 코드를 작성하세요
            # 대문자와 소문자를 구분하여 처리해야 합니다
            pass
        else:
            # 알파벳이 아닌 경우 그대로 추가
            result += char
    
    return result
    """, language="python")
    
    st.write("""
    ### 힌트:
    1. ROT13은 알파벳을 13글자씩 시프트하는 암호입니다.
    2. 대문자와 소문자를 구분하여 처리해야 합니다.
    3. 시저 암호와 유사하지만 시프트 값이 고정되어 있습니다 (13).
    """)
    
    answer = st.text_area("답안 작성:", height=150)
    if st.button("정답 확인"):
        correct_answer1 = "result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))"
        correct_answer2 = "result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))"
        
        if correct_answer1 in answer and correct_answer2 in answer:
            st.success("정답입니다! 올바른 ROT13 변환 코드를 작성했습니다.")
        else:
            st.error("틀렸습니다. 대문자와 소문자를 모두 처리하는지 확인하세요.")

if __name__ == "__main__":
    rot13_app()