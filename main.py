import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chat with Pygent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt.strip()

    if not user_prompt:
        raise ValueError("Empty prompt")

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # return

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if args.verbose:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')
        print(f'Total tokens: {response.usage.total_tokens}')

    message = response.choices[0].message

    if message.tool_calls:
        print("Tools:")
        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call, True)
            print(f"Result:\n\n{result_message["content"]}")

        print("--------- Tools end ---------")
        print("")
    else:
        print("Response:")
        print(message.content)
        print("--------- Response end ---------")
        print("")


if __name__ == "__main__":
    main()
