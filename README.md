# Worker Test - Document Analysis with Azure AI

A Python application that processes PDF documents using Azure Vision API for OCR and Azure OpenAI for intelligent document analysis.

## Features

- **PDF Processing**: Converts PDF pages to images for analysis
- **OCR Processing**: Extracts text from documents using Azure Vision API
- **AI Analysis**: Generates detailed summaries using Azure OpenAI
- **PDF Output**: Creates analysis results as PDF documents

## Requirements

- Python 3.13.9+
- Azure Vision API access
- Azure OpenAI API access

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd worker-test
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Configure your Azure credentials in the `.env` file:
- `AZURE_VISION_API_KEY`: Your Azure Vision API key
- `AZURE_VISION_ENDPOINT`: Your Azure Vision endpoint
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your deployment name (e.g., "gpt-4o")

## Usage

1. Place your PDF file in the `temp/` directory as `sample.pdf`

2. Run the application:
```bash
python main.py
```

3. The application will:
   - Convert the first page of the PDF to an image
   - Extract text using Azure Vision OCR
   - Analyze the content with Azure OpenAI
   - Generate a summary PDF in `temp/analysis_result.pdf`

## Dependencies

- **pydantic**: Data validation and settings management
- **openai**: Azure OpenAI API client
- **azure-ai-vision-imageanalysis**: Azure Vision API for OCR
- **pymupdf**: PDF processing library

## License

This project is for testing and educational purposes.
