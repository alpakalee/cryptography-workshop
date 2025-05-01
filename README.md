# Streamlit 암호학 실습 배포 가이드

이 문서는 암호학 2주차 실습 (브루트 포스 & 빈도 분석)을 Streamlit Community Cloud에 배포하는 방법을 안내합니다.

## 목차
1. [실습 파일 준비](#실습-파일-준비)
2. [GitHub 저장소 생성](#github-저장소-생성)
3. [Streamlit Community Cloud 계정 생성](#streamlit-community-cloud-계정-생성)
4. [앱 배포](#앱-배포)
5. [문제 해결](#문제-해결)

## 실습 파일 준비

실습에 필요한 다음 파일들이 준비되어 있어야 합니다:

- `streamlit_app.py`: 메인 Streamlit 애플리케이션 파일
- `caesar_cipher.py`: 시저 암호 브루트 포스 실습 파일
- `rot13_cipher.py`: ROT13 암호 실습 파일
- `frequency_analysis.py`: 빈도 분석 기반 암호 해독 실습 파일
- `requirements.txt`: 필요한 파이썬 패키지 목록

`requirements.txt` 파일에는 다음 내용이 포함되어야 합니다:
