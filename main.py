import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client, messages, args) -> str | None:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("failed API request")

    message = response.choices[0].message
    reply = ""

    if args.verbose:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        verbose_string = "\n".join(
            [
                f"User prompt: {args.user_prompt}",
                "==============================",
                f"Prompt tokens: {prompt_tokens}",
                f"Response tokens: {completion_tokens}",
                "==============================\n",
            ]
        )
        reply += verbose_string

    if message.tool_calls:
        calls = []
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message["content"]:
                raise Exception("no content in tool response")

            result_string = f"-> {result_message['content']}"
            calls.append(result_string)

        call_string = "\n".join(calls)

        if args.verbose:
            reply += call_string

    else:
        reply += f"Response:\n{message.content}"

    return reply


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{args.user_prompt}, brief answer"},
    ]

    reply = generate_content(client, messages, args)
    print(reply)


if __name__ == "__main__":
    main()
