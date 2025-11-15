from openai.types.chat import ChatCompletionMessageParam
from openai import AzureOpenAI
from typing import Iterable

from shared.date_utils import DateUtils
from core import settings


def analyze_pdf_text(full_text):
    """
    Analyze text extracted from a PDF document using Azure OpenAI.

    :param full_text: The full text extracted from the PDF.
    :return: Analysis result as a Markdown-formatted string.
    """
    llm_api_key = settings.azure_openai_api_key
    llm_endpoint = settings.azure_openai_endpoint
    llm_deployment_name = settings.azure_openai_deployment_name

    if not llm_api_key or not llm_endpoint or not llm_deployment_name:
        raise ValueError("Azure OpenAI settings are not properly configured.")

    llm_client = AzureOpenAI(
        api_key=llm_api_key,
        api_version="2024-06-01",
        azure_endpoint=llm_endpoint,
    )

    llm_execution_time = DateUtils.get_current_utc_time()

    prompt_file_path = "prompts/content_summary.txt"
    prompt_template = ""

    with open(prompt_file_path, "r", encoding="utf-8") as prompt_file:
        prompt_template = prompt_file.read()

    print("📄 Loaded prompt template from prompts/content_summary.txt")

    messages: Iterable[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "You are an assistant specialized in document analysis.",  # System context
        },
        {
            "role": "system",
            "content": (f"{prompt_template}" "Here is the text:\n\n" f"{full_text}"),
        },
    ]

    print("🚀 Starting document analysis with Azure OpenAI...")
    print(f"   Endpoint: {llm_endpoint}")
    print(f"   Deployment: {llm_deployment_name}")

    response = llm_client.chat.completions.create(
        model=llm_deployment_name,
        messages=messages,
        temperature=0,  # Deterministic responses
    )

    print("📄 Documents analyzed successfully!")

    # Extract response
    result_text = response.choices[0].message.content

    llm_completion_time = DateUtils.get_exec_time_seconds(llm_execution_time)

    print("✅ Analysis completed!")
    print(f"   Model: {response.model}")
    print(f"   Execution time: {llm_completion_time} seconds")
    return result_text
