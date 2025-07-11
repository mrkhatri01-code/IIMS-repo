import os
from dotenv import load_dotenv
load_dotenv()

import requests

class CommentaryGenerator:
    """
    Generates natural language commentary for sports highlights using Azure OpenAI or HuggingFace.
    Falls back to dummy commentary if no API credentials are set.
    """
    def __init__(self):
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_token = os.getenv('AZURE_OPENAI_AD_TOKEN')
        self.deployment = os.getenv('DEPLOYMENT_NAME')
        self.api_version = os.getenv('OPENAI_API_VERSION')
        self.hf_token = os.getenv('HUGGINGFACEHUB_ACCESS_TOKEN')

    def generate(self, highlight_desc):
        prompt = (
            f"You are a professional sports commentator. "
            f"Write a short, exciting, and natural-sounding commentary for the following highlight: {highlight_desc}\n"
            f"Keep it under 2 sentences."
        )
        if self.azure_endpoint and self.azure_token:
            return self._azure_openai(prompt)
        elif self.hf_token:
            return self._huggingface_gpt2(prompt)
        else:
            return f"Highlight: {highlight_desc} (dummy commentary)"

    def _azure_openai(self, prompt):
        url = f"{self.azure_endpoint}openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        headers = {"api-key": self.azure_token, "Content-Type": "application/json"}
        data = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 60, "temperature": 0.7}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.ok:
                return resp.json()['choices'][0]['message']['content'].strip()
            else:
                print(f"Azure OpenAI API error: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Azure OpenAI request failed: {e}")
        return "(Failed to generate commentary)"

    def _huggingface_gpt2(self, prompt):
        api_url = "https://api-inference.huggingface.co/models/MatchTime/gpt2-base-sports-commentary"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": prompt}
        try:
            resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
            if resp.ok:
                result = resp.json()
                if isinstance(result, list) and 'generated_text' in result[0]:
                    return result[0]['generated_text'].strip()
                elif isinstance(result, dict) and 'generated_text' in result:
                    return result['generated_text'].strip()
            else:
                print(f"HuggingFace API error: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"HuggingFace request failed: {e}")
        return "(Failed to generate commentary)" 