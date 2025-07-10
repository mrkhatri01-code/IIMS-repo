import os
from dotenv import load_dotenv
load_dotenv()

import requests

class CommentaryGenerator:
    def __init__(self):
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_token = os.getenv('AZURE_OPENAI_AD_TOKEN')
        self.deployment = os.getenv('DEPLOYMENT_NAME')
        self.api_version = os.getenv('OPENAI_API_VERSION')
        self.hf_token = os.getenv('HUGGINGFACEHUB_ACCESS_TOKEN')

    def generate(self, highlight_desc):
        if self.azure_endpoint and self.azure_token:
            return self._azure_openai(highlight_desc)
        elif self.hf_token:
            return self._huggingface_gpt2(highlight_desc)
        else:
            return f"Highlight: {highlight_desc} (dummy commentary)"

    def _azure_openai(self, prompt):
        url = f"{self.azure_endpoint}openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        headers = {"api-key": self.azure_token, "Content-Type": "application/json"}
        data = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 60, "temperature": 0.7}
        resp = requests.post(url, headers=headers, json=data)
        if resp.ok:
            return resp.json()['choices'][0]['message']['content']
        return "(Failed to generate commentary)"

    def _huggingface_gpt2(self, prompt):
        api_url = "https://api-inference.huggingface.co/models/MatchTime/gpt2-base-sports-commentary"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": prompt}
        resp = requests.post(api_url, headers=headers, json=payload)
        if resp.ok:
            return resp.json()[0]['generated_text']
        return "(Failed to generate commentary)" 