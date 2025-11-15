from azure.storage.blob import BlobServiceClient
import asyncio

from shared.file_utils import convert_pdf_pages_to_images_bytes
from shared.vision_utils import extract_text_from_image_bytes
from shared.pdf_utils import PdfConfig, save_markdown_as_pdf
from shared.text_utils import process_text_for_insights
from core.settings import settings


async def execute_pdf_analysis(blob_bytes: bytes, blob_name: str) -> str | None:
    print("🛠️ Starting PDF processing and analysis workflow...")

    # PDF Document Conversion
    image_bytes = convert_pdf_pages_to_images_bytes(blob_bytes)

    # Azure Vision
    all_extracted_texts = []
    for image_byte in image_bytes:
        ocr_text = extract_text_from_image_bytes(image_byte)
        all_extracted_texts.append(ocr_text)

    pdf_ocr_output = "\n".join(all_extracted_texts)

    # LLM
    extracted_insights_as_markdown = process_text_for_insights(
        pdf_ocr_output, "text_summary"
    )

    # Create PDF with results - Convert Markdown to PDF with full formatting

    if extracted_insights_as_markdown:
        analysis_result_path = f"temp/analysis/{blob_name}.pdf"

        # Convert markdown to professionally formatted PDF
        save_markdown_as_pdf(
            extracted_insights_as_markdown,
            analysis_result_path,
            config=PdfConfig(padding_px=0),
        )
        print(f"📄 PDF created with full formatting: {analysis_result_path}")
        return analysis_result_path
    else:
        print("❌ No content to save")
        return None


async def register_listener():
    print("🔔 Registering Azure Blob Storage listener...")

    blob_service_client = BlobServiceClient.from_connection_string(
        settings.storage_connection_string
    )
    container_client = blob_service_client.get_container_client(
        settings.storage_container_name
    )

    # Snapshot inicial
    current_blobs = []
    for blob in container_client.list_blobs():
        current_blobs.append(blob.name)

    print(f"📊 Initial state: {len(current_blobs)} blobs found")

    while True:
        await asyncio.sleep(5)  # Check every 5 seconds

        for blob in container_client.list_blobs():
            if blob.name not in current_blobs:
                print(
                    f"🆕 New blob detected: {blob.name}, Last modified: {blob.last_modified}"
                )
                current_blobs.append(blob.name)

                print(f"📥 Downloading blob: {blob.name}")
                blob_client = container_client.get_blob_client(blob.name)
                blob_data = blob_client.download_blob().readall()

                print(f"⬇️ Blob {blob.name} downloaded, size: {len(blob_data)} bytes")
                blob_name = blob.name.rsplit(".", 1)[0]
                await execute_pdf_analysis(blob_data, blob_name)


if __name__ == "__main__":
    asyncio.run(register_listener())
