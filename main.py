from shared.file_utils import convert_pdf_pages_to_images_bytes
from shared.vision_utils import extract_text_from_image_bytes
from shared.pdf_utils import PdfConfig, save_markdown_as_pdf
from shared.text_utils import analyze_pdf_text


async def main():
    print("🛠️ Starting PDF processing and analysis workflow...")

    # PDF Document Conversion
    image_bytes = convert_pdf_pages_to_images_bytes("temp/sample.pdf")

    # Azure Vision
    full_text = extract_text_from_image_bytes(image_bytes)

    # LLM
    extracted_insights_as_markdown = analyze_pdf_text(full_text)

    # Create PDF with results - Convert Markdown to PDF with full formatting

    if extracted_insights_as_markdown:
        analysis_result_path = "temp/analysis_result.pdf"

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


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
