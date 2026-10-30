import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    parser = argparse.ArgumentParser(description="Chat with Pygent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    user_prompt = args.user_prompt.strip()

    if not user_prompt:
        raise ValueError("Empty prompt")

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
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    print(f'Prompt tokens: {response.usage.prompt_tokens}')
    print(f'Response tokens: {response.usage.completion_tokens}')
    print(f'Total tokens: {response.usage.total_tokens}')

    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
