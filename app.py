import streamlit as st
import base64
from pathlib import Path

# ▶ 배경 이미지 파일 경로
bg_image_path = "background_image_chatGPT.png"
# ▶ 이미지 파일을 base64로 인코딩
encoded = None
p = Path(bg_image_path)
if p.exists():
    encoded = base64.b64encode(p.read_bytes()).decode()

# ▶ CSS 스타일 정의
st.markdown(
    f"""
    <style>
    /* 전체 배경 적용 */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}

    /* 여백 제거 */
    .main {{
        padding-top: 0rem !important;
    }}
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    /* 헤더(세 점 메뉴) 제거 */
    header[data-testid="stHeader"] {{
        visibility: hidden;
        height: 0;
    }}

    /* 사이드바 넓히기 */
    section[data-testid="stSidebar"] {{
        width: 405px !important;
        mid-width: 405px !important;
        background-color: #f0f2f6 !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }}
    /* 사이드바 내부 컨테이너 조정 */
    div[data-testid="stSidebar"] > div:first-child {{
        width: 100% !important;
        padding-top: 0rem !important;
        padding-bottm: 0rem !important;
        overflow-y: auto;
    }}


    /* 사이드바 타이틀 스타일 커스터마이징 */
    .custom-sidebar-title {{
        font-size: 36px;
        font-weight: bold;
        color: #333;
        margin-top: 0rem;
        margin-bottom: 1rem;
    }}

    /* 사이드바 로그인 버튼 커스터마이징 */
    .custom-login-button > button {{
        background-color: rgb(255,82,26) !important;  /* 버튼 배경색 */
        color: white !important;               /* 글자색 */
        width: 100% !important;                /* 전체 폭 */
        border-radius: 5px !important;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        margin-top: 0.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ▶ 페이지 내용
#st.sidebar.title("링크업 Lab") 기본 사이드바X
#st.title("🖼️ 내 이미지 배경 적용 완료")
#st.write("이제 배경은 내 로컬 이미지로 바뀌었고, 사이드바도 더 넓어졌어요.")

st.sidebar.markdown('<div class="custom-sidebar-title">링크업 Lab</div>', unsafe_allow_html=True)

#데모용 사용자 DB(평문, 나중에 수정할 것)
USER_DB={"admin":"admin1234", "guest":"guest1"}

#인증 함수
def authenticate(uid: str, pw :str) -> bool:
  return bool(uid) and USER_DB.get(uid) == pw

#세션 상태 초기화
if "auth" not in st.session_state:
  st.session_state.auth=False
if "user" not in st.session_state:
  st.session_state.auth=None

#로그인
with st.sidebar:
    uid = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    login_clicked = st.button("🔐로그인", type="primary", use_container_width=True)

    if login_clicked:
        if authenticate(uid, pw):
            st.session_state.auth = True
            st.session_state.user = uid
            st.success(f"✅ 로그인 성공: {uid}님 환영합니다!")
            # st.experimental_set_query_params(page="dashboard")  # 선택적(멀티페이지)
            # st.experimental_rerun()
        else:
            st.session_state.auth = False
            st.session_state.user = None
            st.error("❌ 로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다.")

# --- 메인 화면 ---
# if st.session_state.auth:
#     st.write(f"🔓 현재 로그인된 사용자: **{st.session_state.user}**")
# else:
#     st.write("🔒 로그인되지 않았습니다.")
