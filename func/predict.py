import torch
from model import BindingAffinityPredictor
from esm import pretrained
import numpy as np

def load_model(checkpoint_path):
    model, alphabet = pretrained.esm1b_t33_650M_UR50S()
    model.eval()

    affinity_model = BindingAffinityPredictor(esm_model=model, embedding_dim=1280, mlp_hidden_dim=256)
    # affinity_model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')))
    #지금 esm 파트 학습X, 그냥 mlp만 그래서 파라미터 불러올때 수정함.
    affinity_model.mlp.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')))

    affinity_model.eval()
    return affinity_model, alphabet

def get_sequence_embedding(sequence, model, alphabet):
    batch_converter = alphabet.get_batch_converter()
    data = [("seq", sequence)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)

    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=False)
        token_representations = results["representations"][33]

    sequence_embedding = token_representations[0, 1:len(sequence)+1].mean(0)
    return sequence_embedding

def predict_affinity(scfv_seq, antigen_seq, checkpoint_path="mlp_checkpoint.pt"):
    model, alphabet = load_model(checkpoint_path)

    emb1 = get_sequence_embedding(scfv_seq, model.esm, alphabet)
    emb2 = get_sequence_embedding(antigen_seq, model.esm, alphabet)
    
    with torch.no_grad():
        affinity = model(emb1, emb2).item()
    return affinity

# 예시 실행
if __name__ == "__main__":
    scfv = "EVQLVESGGGLVQPGGSLRLSCAASGFTFSSYAMHWVRQAPGKGLEWVSAISSSGSNTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKYYYAMDYWGQGTTVTVSS"
    antigen = "MGHHHHHHSSGVDLGTENLYFQSAMAEGSSVAPVDKVTKLVGQLGYSVKPGASVGVLDVDEAAAMKAALEKASADKPTKEILDGISGKDGRLAFRDALD"
    affinity_score = predict_affinity(scfv, antigen)
    print(f"Predicted Binding Affinity: {affinity_score:.4f}")
