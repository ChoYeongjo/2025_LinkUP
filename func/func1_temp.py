import streamlit as st
import torch
from model import BindingAffinityPredictor

# 모델 로딩
@st.cache_resource
def load_model():
    model = BindingAffinityPredictor()
    #예외처리 일단 사용이 우선. 나중에 처리할것.
    try:
      # # model.load_state_dict(torch.load("mlp_weights.pth", map_location="cpu"))
      # #지금 mlp만 가져와서 붙일 것.
      # model.mlp.load_state_dict(torch.load("mlp_weights.pth", map_location="cpu"))
      # 다시 키값 수정
      # state_dict = torch.load("mlp_weights.pth", map_location="cpu")
      # model.mlp.load_state_dict(state_dict["mlp"])

        state_dict = torch.load("mlp_weights.pth", map_location="cpu")
        new_state_dict = {k.replace("mlp.", ""): v for k, v in state_dict.items()}
        model.mlp.load_state_dict(new_state_dict)
    except FileNotFoundError:
      st.warning("mlp_weights.pth not found. using randomly initialized weights")
    model.eval()
    return model
    
    # model.load_state_dict(torch.load("mlp_weights.pth", map_location="cpu"))  # MLP만 학습된 경우
    # model.eval()
    # return model

model = load_model()

# Streamlit 인터페이스
st.title("🔬 Binding Affinity Predictor")
st.markdown("**scFv (항체) 서열**과 **Antigen (항원) 서열**을 입력하면 바인딩 어피니티 수치를 예측합니다.")

scfv_seq = st.text_area("🧬 scFv Sequence", height=150, placeholder="예: EVQLVESGGGLVQPGGSLRLSCAAS...")
antigen_seq = st.text_area("🧬 Antigen Sequence", height=150, placeholder="예: MGSSHHHHHHSSGLVPRGSHM...")

if st.button("🔍 Predict Binding Affinity"):
    if not scfv_seq.strip() or not antigen_seq.strip():
        st.warning("⚠️ 두 서열을 모두 입력해주세요.")
    else:
        with st.spinner("Predicting..."):
            with torch.no_grad():
                affinity = model(scfv_seq.strip(), antigen_seq.strip())
                st.success(f"🔗 **Predicted Binding Affinity:** {affinity.item():.4f}")
