from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline
)
import torch

class QwenCodeAnalyzer:
    def __init__(self, model_name: str = "Qwen/Qwen1.5-7B-Code"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )

    def generate_response(self, query: str, context: str = None):
        prompt = self._build_prompt(query, context)
        response = self.pipeline(
            prompt,
            max_new_tokens=512,
            temperature=0.3,
            do_sample=True
        )
        return response[0]['generated_text']

    def _build_prompt(self, query, context):
        return f"""Analyze this code context:
{context}

Answer this question:
{query}

Provide detailed explanation with code examples if needed:"""