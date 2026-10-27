import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Failed to fetch API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": f"{args.user_prompt}\nUse one paragraph",
            }
        ],
    )
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    if not response.usage:
        raise RuntimeError("failed API request")

    print(
        f"Prompt tokens: {prompt_tokens}\nResponse tokens: {completion_tokens}\n\nResponse:"
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
