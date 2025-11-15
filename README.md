# Worker Test - Document Analysis with Azure AI

A Python application that automatically processes PDF documents uploaded to Azure Blob Storage using Azure Vision API for OCR and Azure OpenAI for intelligent document analysis.

## Features

- **Azure Blob Storage Integration**: Monitors storage container for new PDF uploads
- **Real-time Processing**: Automatically detects and processes new files every 5 seconds
- **PDF to Image Conversion**: Converts all PDF pages to high-quality images
- **OCR Processing**: Extracts text from document images using Azure Vision API
- **AI-Powered Analysis**: Generates comprehensive summaries using Azure OpenAI GPT-4o
- **Professional PDF Output**: Creates beautifully formatted analysis reports as PDF files

## Requirements

- Python 3.13.9+
- Azure Blob Storage account
- Azure Vision API access
- Azure OpenAI API access (GPT-4o deployment)

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

4. Configure your Azure credentials in the `.env` file.

## Docker

This application includes a Dockerfile for containerized deployment.

### Running with Docker

1. Build the Docker image:

```bash
docker build -t document-analyzer .
```

2. Run the container using your `.env` file:

```bash
docker run -d --name document-analyzer --env-file .env document-analyzer:latest
```

## Usage

1. Start the application:

```bash
poetry run python main.py
```

2. Upload a PDF file to your configured Azure Blob Storage container

3. The application will automatically:
   - Detect the new file upload
   - Download and convert all PDF pages to images
   - Extract text using Azure Vision OCR
   - Analyze the content with Azure OpenAI
   - Generate a professionally formatted analysis report
   - Save the result as `temp/analysis/{filename}.pdf`

## How It Works

1. **Blob Storage Monitoring**: The application continuously monitors your Azure Blob Storage container for new PDF uploads
2. **Document Processing**: When a new PDF is detected, it's downloaded and converted to high-resolution images
3. **Text Extraction**: Azure Vision API processes each page to extract text with OCR
4. **AI Analysis**: The extracted text is sent to Azure OpenAI GPT-4o for comprehensive analysis
5. **Report Generation**: The AI response is converted from Markdown to a professionally styled PDF report

## Dependencies

- **pydantic** + **pydantic-settings**: Configuration management and validation
- **azure-storage-blob**: Azure Blob Storage integration
- **azure-ai-vision-imageanalysis**: Azure Vision API for OCR
- **openai**: Azure OpenAI API client
- **pymupdf**: PDF processing and image conversion
- **weasyprint** + **markdown**: PDF generation with professional styling

## License

This project is for testing and educational purposes.
