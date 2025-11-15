from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

from core import settings


def extract_text_from_image_bytes(image_bytes: bytearray):
    vision_endpoint = settings.azure_vision_endpoint
    vision_api_key = settings.azure_vision_api_key

    if not vision_api_key or not vision_endpoint:
        raise ValueError("Azure Vision API key and endpoint must be set in settings.")

    vision_client = ImageAnalysisClient(
        endpoint=vision_endpoint, credential=AzureKeyCredential(vision_api_key)
    )

    vision_response = vision_client.analyze(
        image_data=image_bytes, visual_features=[VisualFeatures.READ], language="en"
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

    return full_text
