from dotenv import load_dotenv
from openai import AzureOpenAI
import os

import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load .env if running locally
load_dotenv()

# Read Azure OpenAI config
AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]
EMBEDDING_DEPLOYMENT = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
)


def embed_text(text: str):
    """
    Takes a string and returns its embedding vector.
    """
    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding


def main():
    # Load questions.json
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Process each question
    for item in questions:
        q_text = item.get("question", "")

        if not q_text:
            print("Warning: Question missing, skipping entry.")
            continue

        print(f"Embedding question: {q_text}")

        embedding = embed_text(q_text)

        # Save embedding inside the JSON object
        item["embedded_question"] = embedding

    # Save output file
    output_path = "questions_with_embeddings.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Saved embedded questions to: {output_path}")


if __name__ == "__main__":
    main()