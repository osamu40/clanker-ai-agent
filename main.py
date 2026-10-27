import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


def generate_content(client, messages) -> str:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError("failed API request")

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}\n")
    print("Response:")

    return response.choices[0].message.content


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

    messages = [
        {"role": "user", "content": f"{args.user_prompt}, short answer"},
    ]

    reply = generate_content(client, messages)
    print(reply)


if __name__ == "__main__":
    main()
