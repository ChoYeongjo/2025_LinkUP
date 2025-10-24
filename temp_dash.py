import streamlit as st
import base64
from pathlib import Path

# def load_icon_as_base64(path: str) -> str:
#     with open(path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# 임시로 하나만
ICON_PATH="images/temp_icon.png"
encoded = None
p = Path(ICON_PATH)

if p.exists():
    encoded = base64.b64encode(p.read_bytes()).decode()

    
ICON_TAG =  f'<img src="data:image/png;base64,{encoded}" alt="icon_error" />'

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
st.title("Dashboard")

# ---------- CSS ----------
st.markdown("""
<style>
.section-title{font-size: 22px; font-weight: 700; margin: 1px 0 10px;}
.section-divider{height: 0;border-top: 3px solid #5da350;margin: 26px 0 18px;opacity: .8;}

/*왼쪽부터 붙고, 넘으면 아래로(flexiable) */
.row{
    display: flex; flex-wrap: wrap; gap: 24px; justify-content: flex-start;
}
/* 카드 */
.card{
    position:relative;
    width: 200px; height: 180px;
    border: 1.2px solid rgba(0,0,0,0.15);
    border-radius: 10px; background: #fff;
    text-align: center; padding: 12px 8px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    cursor: pointer;
}
.card:hover{ transform: translateY(-2px); box-shadow: 0 6px 14px rgba(0,0,0,0.12);}
.card img{ height: 100px; width: auto; margin-bottom: 8px;}
.card p{ font-size: 17px; font-weight: 600; margin: 0; line-height: 1.3;}
.card.disabled{ opacity: 0.60; cursor: not-allowed; filter:grayscale(35%)}

/* ✅ 카드 전체 클릭 영역(투명 버튼) -> 역할 정확히? */
.card form { position:absolute; inset:0; margin:0; }
.card form .stButton { position:absolute; inset:0; margin:0; }
.card form .stButton > button {
  position:absolute; inset:0; width:100% !important; height:100% !important;
  opacity:0 !important; border:none !important; background:transparent !important;
  cursor:pointer !important;
}

/* 주석 */
.note{font-size: 13px; color: #666; margin-top: 4px;}
</style>
""", unsafe_allow_html=True)

# 카드렌더함수
def card(label_html: str, icon_tag: str, key: str, target_page: str|None, disabled: bool=False):
    disabled_cls = " disabled" if disabled else ""
    st.markdown(
        f'<div class="card{disabled_cls}">'
        f'{icon_tag}'
        f'<p>{label_html}</p>',
        unsafe_allow_html=True
    )
    if not disabled and target_page:
        with st.form(f"form_{key}"):
            go = st.form_submit_button("go")   # 투명 전체버튼
        if go:
            st.switch_page(target_page)
    else:
        st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------
# Section 1: Antigen-Antibody Reaction
# --------------------------
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Antigen–Antibody Reaction</div>', unsafe_allow_html=True)

cards_html = []
cards_html.append(f"""
  <div class="card">
    {ICON_TAG}
    <p>Binding Affinity<br>(only sequence)</p>
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">1차년도 개발 완성</div>  
  </div>
""")
cards_html.append(f"""
  <div class="card disabled">
    {ICON_TAG}
    <p>Binding Affinity<br>(+ 3D structure)</p>
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">2차년도 개발 예정</div>
  </div>  
""")
cards_html.append(f"""
  <div class="card disabled">
    {ICON_TAG}
    <p>Binding Sites<br>(Paratope / Epitope)</p>
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">2차년도 개발 예정</div>    
  </div>
""")
st.markdown(f'<div class="row">{"".join(cards_html)}</div>', unsafe_allow_html=True)

# --------------------------
# Section 2: Therapeutic forecasting
# --------------------------
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Therapeutic forecasting</div>', unsafe_allow_html=True)

cards_html = []
cards_html.append(f"""
  <div class="card">
    {ICON_TAG}
    <p>CRS Risk Scan<br>(Design Phrase)</p>
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">1차년도 개발 완성</div>
  </div>
""")
cards_html.append(f"""
  <div class="card">
    {ICON_TAG}
    <p>CRS Risk Scan<br>(Post-Infusion)</p>
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">1차년도 개발 완성</div>
  </div>
""")
cards_html.append(f"""
  <div class="card disabled">
    {ICON_TAG}
    <p>DOR prediction<br>(Duration of Response)</p>  
    <div class="note" style="font-size: 16px; padding-left: 8px; margin-top:14px;">2차년도 개발 예정</div>
  </div>

""")

st.markdown(f'<div class="row">{"".join(cards_html)}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.caption("향후 기능들이 완성되면 활성화 및 추가 생성될 예정입니다.")