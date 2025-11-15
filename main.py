import asyncio

from core import storage, settings
from shared.file_utils import convert_pdf_pages_to_images_bytes
from shared.vision_utils import extract_text_from_image_bytes
from shared.pdf_utils import PdfConfig, convert_markdown_to_pdf
from shared.text_utils import process_text_for_insights


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
        # Convert markdown to professionally formatted PDF
        analysis_result_pdf_bytes = convert_markdown_to_pdf(
            extracted_insights_as_markdown,
            config=PdfConfig(padding_px=0),
        )

        # Save PDF to Azure Blob Storage
        analysis_prefix = settings.storage_blob_analyzed_prefix
        analysis_result_path = f"{analysis_prefix}{blob_name}_analysis.pdf"
        await storage.upload_blob(analysis_result_path, analysis_result_pdf_bytes)

        print(f"📄 PDF created with full formatting: {analysis_result_path}")
    else:
        print("❌ No content to save")
        return None


async def register_listener():
    print("🔔 Registering Azure Blob Storage listener...")

    file_prefix = settings.storage_blob_to_analyze_prefix

    # Snapshot inicial
    current_blobs = []
    async for blob in await storage.list_blobs(name_starts_with=file_prefix):
        blob_name = blob.name.rsplit(".", 1)[0]
        current_blobs.append(blob_name)

    print(f"📊 Initial state: {len(current_blobs)} blobs found")

    while True:
        await asyncio.sleep(5)  # Check every 5 seconds

        async for blob in await storage.list_blobs(name_starts_with=file_prefix):
            blob_name = blob.name.rsplit(".", 1)[0]

            if blob_name not in current_blobs:

                print(
                    f"🆕 New blob detected: {blob_name}, Last modified: {blob.last_modified}"
                )
                current_blobs.append(blob_name)

                print(f"📥 Downloading blob: {blob_name}")
                blob_data = await storage.download_blob(blob.name)

                blob_name_without_prefix = blob_name[len(file_prefix) :]

                print(f"⬇️ Blob {blob_name} downloaded, size: {len(blob_data)} bytes")
                await execute_pdf_analysis(blob_data, blob_name_without_prefix)


if __name__ == "__main__":
    asyncio.run(register_listener())
