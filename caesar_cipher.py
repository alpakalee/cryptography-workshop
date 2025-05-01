# 2week/caesar_cipher.py

import streamlit as st
import pandas as pd
import string
import base64
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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

def create_cipher_wheel(shift):
    """
    시저 암호 회전판을 시각화하는 이미지를 생성합니다.
    
    매개변수:
        shift (int): 시프트 값 (0-25)
    
    반환값:
        Image: 시저 암호 회전판 이미지
    """
    # 이미지 크기 설정
    width, height = 500, 500
    center = (width // 2, height // 2)
    
    # 이미지 생성
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 원 그리기
    outer_radius = 200
    inner_radius = 150
    draw.ellipse((center[0] - outer_radius, center[1] - outer_radius, 
                 center[0] + outer_radius, center[1] + outer_radius), 
                 outline='black')
    draw.ellipse((center[0] - inner_radius, center[1] - inner_radius, 
                 center[0] + inner_radius, center[1] + inner_radius), 
                 outline='black')
    
    # 폰트 설정
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # 바깥 원에 알파벳 그리기
    alphabet = string.ascii_uppercase
    for i, letter in enumerate(alphabet):
        angle = 360 / len(alphabet) * i
        angle_rad = angle * math.pi / 180
        
        r = (outer_radius + inner_radius) // 2
        x = center[0] + int(r * 0.8 * math.sin(angle_rad))
        y = center[1] - int(r * 0.8 * math.cos(angle_rad))
        
        # 텍스트 위치 조정
        text_width = font.getsize(letter)[0] if hasattr(font, 'getsize') else 10
        text_height = font.getsize(letter)[1] if hasattr(font, 'getsize') else 10
        draw.text((x - text_width//2, y - text_height//2), letter, fill='blue', font=font)
    
    # 안쪽 원에 시프트된 알파벳 그리기
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    for i, letter in enumerate(shifted_alphabet):
        angle = 360 / len(shifted_alphabet) * i
        angle_rad = angle * math.pi / 180
        
        r = inner_radius // 2
        x = center[0] + int(r * 0.8 * math.sin(angle_rad))
        y = center[1] - int(r * 0.8 * math.cos(angle_rad))
        
        # 텍스트 위치 조정
        text_width = font.getsize(letter)[0] if hasattr(font, 'getsize') else 10
        text_height = font.getsize(letter)[1] if hasattr(font, 'getsize') else 10
        draw.text((x - text_width//2, y - text_height//2), letter, fill='red', font=font)
    
    # 회전 화살표 그리기
    draw.line([center, (center[0], center[1] - outer_radius - 20)], fill='green', width=2)
    text_width = font.getsize(f"시프트: {shift}")[0] if hasattr(font, 'getsize') else 80
    draw.text((center[0] - text_width//2, center[1] - outer_radius - 60), f"시프트: {shift}", fill='black', font=font)
    
    return image

def get_image_download_link(img, filename, text):
    """
    이미지를 다운로드할 수 있는 링크를 생성합니다.
    """
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def caesar_cipher_app():
    st.title("시저 암호 브루트 포스 공격")
    
    st.write("""
    ### 시저 암호란?
    시저 암호는 각 글자를 알파벳 상에서 일정한 수만큼 이동시키는 암호화 방식입니다.
    예를 들어, 시프트 값이 3이면 'A'는 'D'로, 'B'는 'E'로 암호화됩니다.
    """)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Caesar_cipher_left_shift_of_3.svg/1200px-Caesar_cipher_left_shift_of_3.svg.png", 
            caption="시저 암호 시프트 다이어그램")
    
    st.write("""
    ### 브루트 포스(무차별 대입) 공격이란?
    가능한 모든 키(시저 암호의 경우 시프트 값 1-25)를 시도하여 원문을 찾아내는 방법입니다.
    """)
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["브루트 포스 공격", "암호화/복호화", "시각적 학습", "시저 암호 퍼즐"])
    
    with tab1:
        st.header("브루트 포스 공격")
        ciphertext = st.text_area("암호문을 입력하세요:", "DWWDFN DW GDZQ", height=100)
        
        if st.button("브루트 포스 공격 실행", key="brute_force_btn"):
            results = brute_force_caesar(ciphertext)
            
            st.write("### 모든 가능한 시프트 값에 대한 결과:")
            
            # 결과를 더 직관적으로 표시
            results_df = pd.DataFrame({
                "시프트": [r[0] for r in results],
                "복호화 결과": [r[1] for r in results]
            })
            
            st.dataframe(results_df)
            
            # 빈도 분석 도움말
            st.info("""
            💡 **도움말**: 영어에서 가장 자주 사용되는 알파벳은 E, T, A, O, I, N 순서입니다.
            암호문에서 가장 자주 나타나는 문자를 찾아 이것이 E일 가능성이 높다고 가정하면 
            시프트 값을 더 쉽게 찾을 수 있습니다.
            """)
    
    with tab2:
        st.header("암호화/복호화")
        
        mode = st.radio("모드 선택:", ["암호화", "복호화"])
        
        text = st.text_area("텍스트 입력:", "ATTACK AT DAWN" if mode == "암호화" else "DWWDFN DW GDZQ", height=100)
        shift = st.slider("시프트 값 (1-25):", 1, 25, 3)
        
        if st.button("실행", key="encrypt_decrypt_btn"):
            if mode == "암호화":
                result = caesar_encrypt(text, shift)
                st.success(f"암호화 결과: {result}")
            else:
                result = caesar_decrypt(text, shift)
                st.success(f"복호화 결과: {result}")
    
    with tab3:
        st.header("시각적 학습")
        
        st.write("""
        ### 시저 암호 회전판
        아래 슬라이더를 조절하여 시프트 값을 변경해보세요. 
        바깥쪽 원의 파란색 알파벳이 원본이고, 안쪽 원의 빨간색 알파벳이 암호화된 결과입니다.
        """)
        
        viz_shift = st.slider("회전판 시프트 값:", 0, 25, 3, key="viz_shift")
        
        try:
            # 시저 암호 회전판 이미지 생성
            wheel_img = create_cipher_wheel(viz_shift)
            st.image(wheel_img, caption=f"시저 암호 회전판 (시프트: {viz_shift})", use_column_width=True)
            
            # 다운로드 링크 제공
            st.markdown(get_image_download_link(wheel_img, f"caesar_wheel_{viz_shift}.png", "회전판 이미지 다운로드"), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
        
        # 간단한 연습 문제
        st.write("### 연습 문제")
        practice_text = "HELLO"
        st.write(f"원본 텍스트: {practice_text}")
        st.write(f"시프트 {viz_shift}로 암호화한 결과: {caesar_encrypt(practice_text, viz_shift)}")
        
        user_answer = st.text_input("위 텍스트를 직접 암호화해보세요:", key="practice_answer")
        
        if st.button("정답 확인", key="check_practice"):
            correct = caesar_encrypt(practice_text, viz_shift)
            if user_answer.upper() == correct.upper():
                st.success(f"정답입니다! {practice_text}를 시프트 {viz_shift}로 암호화하면 {correct}가 됩니다.")
            else:
                st.error(f"틀렸습니다. 정답은 {correct}입니다. 회전판을 참고하여 다시 시도해보세요.")
    
    with tab4:
        st.header("시저 암호 퍼즐")
        
        st.write("""
        ### 암호문 해독 퍼즐
        아래는 시저 암호로 암호화된 메시지입니다. 시프트 값을 조절하여 올바른 메시지를 찾아보세요.
        """)
        
        # 퍼즐에 사용할 암호문 및 시프트 값
        puzzle_ciphers = {
            "퍼즐 1": {"cipher": "FRGH LV IXQ", "shift": 3, "hint": "프로그래밍과 관련된 짧은 문구입니다."},
            "퍼즐 2": {"cipher": "FUBSWRJUDSKB", "shift": 3, "hint": "우리가 배우고 있는 학문입니다."},
            "퍼즐 3": {"cipher": "QEB NRFZH YOLTK CLU", "shift": 23, "hint": "영어 타자 연습에 자주 사용되는 문장의 일부입니다."}
        }
        
        selected_puzzle = st.selectbox("퍼즐 선택:", list(puzzle_ciphers.keys()))
        
        puzzle_data = puzzle_ciphers[selected_puzzle]
        st.write(f"암호문: **{puzzle_data['cipher']}**")
        
        if st.button("힌트 보기", key="hint_btn"):
            st.info(f"힌트: {puzzle_data['hint']}")
        
        puzzle_shift = st.slider("시프트 값 조절:", 1, 25, 1, key="puzzle_shift")
        decrypted = caesar_decrypt(puzzle_data['cipher'], puzzle_shift)
        
        st.write(f"현재 복호화 결과: **{decrypted}**")
        
        # 정답 확인 - 틀렸을 때 원문이 나오지 않도록 수정
        if st.button("정답 확인", key="check_puzzle"):
            correct_shift = puzzle_data['shift']
            
            if puzzle_shift == correct_shift:
                correct_answer = caesar_decrypt(puzzle_data['cipher'], correct_shift)
                st.success(f"정답입니다! 시프트 값 {correct_shift}을(를) 찾았습니다. 원문: {correct_answer}")
            else:
                st.error(f"틀렸습니다. 다른 시프트 값을 시도해보세요.")
        
        # 알파벳 조합 실습
        st.write("### 알파벳 매핑 실습")
        st.write("암호문의 각 글자가 어떤 글자로 바뀌었는지 추측해보세요:")
        
        # 인터랙티브 요소 추가
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**암호문 글자:**")
            for char in puzzle_data['cipher'][:5]:
                if char.isalpha():
                    st.code(char)
        
        with col2:
            st.write("**복호화된 글자 (추측):**")
            for i, char in enumerate(puzzle_data['cipher'][:5]):
                if char.isalpha():
                    st.text_input("", key=f"guess_{i}", max_chars=1)
        
        if st.button("조합 확인", key="check_combo"):
            correct_shift = puzzle_data['shift']
            correct_plain = caesar_decrypt(puzzle_data['cipher'], correct_shift)
            
            # 정답이 바로 표시되지 않고, 사용자의 입력이 맞는지만 확인
            user_correct = True
            plain_chars = []
            
            for i, char in enumerate(puzzle_data['cipher'][:5]):
                if char.isalpha():
                    guess_key = f"guess_{i}"
                    user_guess = st.session_state.get(guess_key, "").upper()
                    correct_char = correct_plain[i].upper()
                    plain_chars.append(correct_char if user_guess == correct_char else "?")
                    
                    if user_guess != correct_char:
                        user_correct = False
            
            if user_correct:
                st.success("모든 문자를 올바르게 맞추셨습니다!")
                st.write(f"정답: **{correct_plain[:5]}**")
            else:
                st.error("일부 또는 모든 문자가 틀렸습니다. 다시 시도해보세요.")
                # 사용자가 맞춘 문자만 보여주고 틀린 문자는 ?로 표시
                st.write(f"현재 결과: **{''.join(plain_chars)}**")
            
            st.write("실습을 완료했으면 브루트 포스 탭으로 돌아가 더 어려운 암호문에 도전해보세요.")

if __name__ == "__main__":
    caesar_cipher_app()