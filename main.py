from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from openai.types.chat import ChatCompletionMessageParam
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from typing import Iterable
import fitz


from shared.date_utils import DateUtils
from core import settings


async def main():
    llm_api_key = settings.azure_openai_api_key
    llm_endpoint = settings.azure_openai_endpoint
    llm_deployment_name = settings.azure_openai_deployment_name

    vision_api_key = settings.azure_vision_api_key
    vision_endpoint = settings.azure_vision_endpoint

    if (
        not llm_api_key
        or not llm_endpoint
        or not llm_deployment_name
        or not vision_api_key
        or not vision_endpoint
    ):
        print("❌ Missing environment variables!")
        return

    # PDF Document Conversion
    pdf_document = fitz.open("temp/sample.pdf")

    first_page = pdf_document.load_page(0)

    pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))

    png_bytes = pix.tobytes("png")

    pdf_document.close()

    with open("temp/page.png", "wb") as img_file:
        img_file.write(png_bytes)
        print("Saved page.png")

    # Azure Vision

    vision_client = ImageAnalysisClient(
        endpoint=vision_endpoint, credential=AzureKeyCredential(vision_api_key)
    )

    vision_response = vision_client.analyze(
        image_data=png_bytes, visual_features=[VisualFeatures.READ], language="en"
    )

    extracted_text = []
    if vision_response.read and vision_response.read.blocks:
        for block in vision_response.read.blocks:
            for line in block.lines:
                extracted_text.append(line.text)

    full_text = "\n".join(extracted_text)

    print(f"✅ Completed OCR!")
    print(
        f"   Blocks found: {len(vision_response.read.blocks) if vision_response.read else 0}"
    )
    print(f"   Text lines: {len(extracted_text)}")
    print(f"   Total characters: {len(full_text)}")

    # LLM

    llm_client = AzureOpenAI(
        api_key=llm_api_key,
        api_version="2024-06-01",
        azure_endpoint=llm_endpoint,
    )

    llm_execution_time = DateUtils.get_current_utc_time()

    messages: Iterable[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": "You are an assistant specialized in document analysis.",  # System context
        },
        {
            "role": "system",
            "content": (
                "Analyze the following text extracted from a PDF document and provide a detailed summary. "
                "It will be saved in a PDF, so only send plain text.\n"
                "Here is the text:\n\n"
                f"{full_text}"
            ),
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

    # Create PDF with results
    pdf_output = fitz.open()
    page = pdf_output.new_page()
    text_lines = result_text.split("\n") if result_text else []
    text_height = 12  # Height of each line
    for i, line in enumerate(text_lines):
        page.insert_text((72, 72 + i * text_height), line, fontsize=10)

    analysis_result_path = "temp/analysis_result.pdf"

    pdf_output.save(analysis_result_path)
    pdf_output.close()

    return analysis_result_path


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
