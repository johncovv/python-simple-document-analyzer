from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML, CSS
from pydantic import BaseModel
import markdown


class PdfConfig(BaseModel):
    """Configuration for PDF generation"""

    # Padding/Margins
    padding_px: int = 20
    margin_top_cm: float = 2.0
    margin_bottom_cm: float = 2.0
    margin_left_cm: float = 2.0
    margin_right_cm: float = 2.0

    # Font settings
    font_family: str = "Arial, sans-serif"
    font_size_pt: int = 12
    line_height: float = 1.6

    # Color scheme
    text_color: str = "#333"
    h1_color: str = "#2c3e50"
    h2_color: str = "#34495e"
    h3_color: str = "#7f8c8d"
    accent_color: str = "#3498db"

    # Page settings
    page_width_mm: int = 210  # A4 width
    page_height_mm: int = 297  # A4 height


def save_markdown_as_pdf(
    markdown_text: str, output_path: str, config: PdfConfig = PdfConfig()
) -> str:
    """
    Convert Markdown to PDF with full formatting using weasyprint

    :param markdown_text: The Markdown text to convert.
    :param output_path: The output PDF file path.
    :param config: PdfConfig object with formatting settings. (Optional)
    :return: The output PDF file path.
    """
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=["extra"])

    # Create a complete HTML document with CSS styling
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Document Analysis</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Calculate total margins (page margins + body padding)
    total_margin_top = config.margin_top_cm + (
        config.padding_px * 0.0353
    )  # Convert px to cm
    total_margin_bottom = config.margin_bottom_cm + (config.padding_px * 0.0353)
    total_margin_left = config.margin_left_cm + (config.padding_px * 0.0353)
    total_margin_right = config.margin_right_cm + (config.padding_px * 0.0353)

    # Build CSS string with config values
    css_content = f"""
        @page {{
            size: {config.page_width_mm}mm {config.page_height_mm}mm;
            margin-top: {total_margin_top}cm;
            margin-bottom: {total_margin_bottom}cm;
            margin-left: {total_margin_left}cm;
            margin-right: {total_margin_right}cm;
        }}

        body {{
            font-family: {config.font_family};
            font-size: {config.font_size_pt}pt;
            line-height: {config.line_height};
            margin: 0;
            padding: 0;
            color: {config.text_color};
        }}

        h1 {{
            color: {config.h1_color};
            font-size: {config.font_size_pt + 6}pt;
            margin-top: 24pt;
            margin-bottom: 12pt;
            border-bottom: 2px solid {config.accent_color};
            padding-bottom: 6pt;
        }}

        h2 {{
            color: {config.h2_color};
            font-size: {config.font_size_pt + 4}pt;
            margin-top: 20pt;
            margin-bottom: 10pt;
        }}

        h3 {{
            color: {config.h3_color};
            font-size: {config.font_size_pt + 2}pt;
            margin-top: 16pt;
            margin-bottom: 8pt;
        }}

        p {{
            margin-bottom: 10pt;
            text-align: justify;
        }}

        ul, ol {{
            margin-bottom: 10pt;
            padding-left: 20pt;
        }}

        li {{
            margin-bottom: 4pt;
        }}

        strong {{
            font-weight: bold;
            color: {config.h1_color};
        }}

        em {{
            font-style: italic;
            color: {config.h3_color};
        }}

        code {{
            background-color: #f8f9fa;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-family: "Courier New", monospace;
        }}

        blockquote {{
            border-left: 4px solid {config.accent_color};
            margin-left: 0;
            padding-left: 16pt;
            font-style: italic;
            color: {config.h3_color};
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 12pt;
        }}

        th, td {{
            border: 1px solid #bdc3c7;
            padding: 8pt;
            text-align: left;
        }}

        th {{
            background-color: #ecf0f1;
            font-weight: bold;
        }}
    """

    css_styles = CSS(string=css_content)

    # Font configuration for better rendering
    font_config = FontConfiguration()

    # Create PDF from HTML
    HTML(string=html_document).write_pdf(
        output_path,
        stylesheets=[css_styles],
        font_config=font_config,
    )

    return output_path
