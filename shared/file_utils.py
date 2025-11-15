import fitz


def convert_pdf_pages_to_images_bytes(pdf_path: str, zoom: float = 2.0) -> bytearray:
    """
    Convert a specific page of a PDF document to a PNG image.

    :param pdf_path: Path to the PDF document.
    :param zoom: Zoom factor for the image quality.
    :return: PNG image bytes.
    """
    pdf_document = fitz.open(pdf_path)
    pdf_pages_count = pdf_document.page_count

    png_images = bytearray()

    for page_number in range(pdf_pages_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        png_images.extend(pix.tobytes("png"))

    pdf_document.close()

    return png_images
