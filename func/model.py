import torch
import torch.nn as nn
import esm

class BindingAffinityPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        # Load pretrained ESM model and alphabet
        self.esm_model, self.alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
        self.batch_converter = self.alphabet.get_batch_converter()

        # Freeze the ESM model (no gradient updates)
        for param in self.esm_model.parameters():
            param.requires_grad = False

        # Set embedding dim manually (ESM-1b: 1280)
        embedding_dim = 1280 * 2  # scfv + antigen concat

        # Simple MLP head for regression
        self.mlp = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 1)
        )

    def forward(self, scfv_seq, antigen_seq):
        # Prepare sequences
        data = [("scfv", scfv_seq), ("antigen", antigen_seq)]
        batch_labels, batch_strs, batch_tokens = self.batch_converter(data)

        # Extract ESM embeddings (use CLS token representation)
        with torch.no_grad():
            results = self.esm_model(batch_tokens, repr_layers=[33], return_contacts=False)

        token_representations = results["representations"][33]  # shape: [2, L, 1280]
        scfv_embedding = token_representations[0, 0]  # [CLS] token (1st token)
        antigen_embedding = token_representations[1, 0]

        # Concatenate embeddings
        combined = torch.cat((scfv_embedding, antigen_embedding), dim=-1)

        # Predict binding affinity
        affinity = self.mlp(combined)
        return affinity
