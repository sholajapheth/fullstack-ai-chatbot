import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()


class GPT:
    def __init__(self):
        self.url = os.environ.get("MODEL_URL")
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINFACE_INFERENCE_TOKEN')}"
        }
        self.payload = {
            "inputs": "",
            "parameters": {
                "return_full_text": False,
                "use_cache": False,
                "max_new_tokens": 25,
            },
        }

    def query(self, input: str) -> list:
        print("query")
        self.payload["inputs"] = input
        response = requests.post(self.url, headers=self.headers, json=self.payload)
        text = response.json()[0]["generated_text"]
        res = str(text.split("Human:")[0]).strip("\n").strip()

        print(res)
        return res


if __name__ == "__main__":
    GPT().query("Will artificial intelligence help humanity conquer the universe?")
