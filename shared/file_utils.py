from uuid import uuid4
import fitz

from core import settings


def convert_pdf_pages_to_images_bytes(
    pdf_bytes: bytes, zoom: float = 2.0
) -> list[bytes]:
    """
    Convert a specific page of a PDF document to a PNG image.

    :param pdf_bytes: PDF document data in bytes.
    :param zoom: Zoom factor for the image quality.
    :return: PNG image bytes.
    """
    pdf_document = fitz.open("pdf", pdf_bytes)
    pdf_pages_count = pdf_document.page_count

    png_images = []

    file_id = str(uuid4())[:8]

    for page_number in range(pdf_pages_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        png_bytes = pix.tobytes("png")
        png_images.append(png_bytes)

        print(f"Converted page {page_number + 1}/{pdf_pages_count} to PNG")

        if settings.is_development:
            # save image for testing
            with open(f"temp/images/{file_id}_page_{page_number + 1}.png", "wb") as f:
                f.write(png_bytes)

            print(f"Saved temp/images/{file_id}_page_{page_number + 1}.png")

    pdf_document.close()

    print(f"✅ Completed PDF to PNG conversion for {pdf_pages_count} pages")

    return png_images
