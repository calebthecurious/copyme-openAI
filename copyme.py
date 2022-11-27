import os

import openai
import argparse
import re

MAX_INPUT_LENGTH = 32


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_copy_snippet(user_input)
        generate_keywords(user_input)
        generate_synonyms(user_input)

    else:
        raise ValueError(f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}"
                         )


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generate_copy_snippet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service

    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding copy for {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)

    # Extract output text.
    copy_text = response["choices"][0]["text"]

    # Strip whitespace from response
    copy_text = copy_text.strip()

    # Add ... to truncate statements
    last_char = copy_text[-1]

    if last_char not in {".", "!", "?"}:
        copy_text += "..."

    print(f"Snippet: {copy_text}")
    return copy_text


def generate_keywords(prompt: str) -> list[str]:
    # Load your API key from an environment variable or secret management service

    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding keywords for {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)

    # Extract output text.
    keywords_text = response["choices"][0]["text"]
    keywords_array = re.split(",|\n\|*|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array if len(k) > 0]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    # Strip whitespace from response
    copy_text = keywords_text.strip()

    print(f"keywords: {keywords_array}")
    return keywords_array


def generate_synonyms(prompt: str) -> list[str]:
    # Load your API key from an environment variable or secret management service

    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate synonyms for {prompt}:"
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)

    # Extract output text.
    synonyms_text = response["choices"][0]["text"]
    synonyms_array = re.split(",|\n\|*|-", synonyms_text)
    synonyms_array = [k.lower().strip()
                      for k in synonyms_array if len(k) > 0]
    keywords_array = [k for k in synonyms_array if len(k) > 0]

    # Strip whitespace from response
    copy_text = synonyms_text.strip()

    print(f"synonyms: {synonyms_array}")
    return synonyms_array


if __name__ == '__main__':
    main()
