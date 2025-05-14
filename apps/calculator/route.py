from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image
import logging

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    try:
        # Decode base64 image data
        if not data.image.startswith("data:image/"):
            raise HTTPException(status_code=400, detail="Invalid image format")
            
        image_data = base64.b64decode(data.image.split(",")[1])
        image_bytes = BytesIO(image_data)
        
        # Open and validate image
        image = Image.open(image_bytes)
        image.verify()  # Verify image integrity
        
        # Process image
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        
        # Collect and log responses
        result_data = []
        for response in responses:
            result_data.append(response)
            logging.info(f"Processed response: {response}")  # Proper logging instead of print
        
        return {
            "message": "Image processed successfully",
            "data": result_data,
            "status": "success"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        ) from e
