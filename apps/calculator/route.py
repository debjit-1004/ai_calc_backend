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
        # Validate image format
        if not data.image.startswith("data:image/"):
            raise HTTPException(status_code=400, detail="Invalid image format. Expected base64 image data URL.")

        # Split and decode base64 data
        header, encoded = data.image.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        # Verify image integrity
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                img.verify()  # Verify without loading pixel data
        except Exception as verify_error:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(verify_error)}") from verify_error

        # Re-open image for processing
        with Image.open(BytesIO(image_bytes)) as img:
            # Convert to compatible format
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            
            # Create fresh in-memory file
            processed_buffer = BytesIO()
            img.save(processed_buffer, format="PNG")
            processed_buffer.seek(0)  # Reset buffer position
            
            # Process image with fresh buffer
            responses = analyze_image(Image.open(processed_buffer), dict_of_vars=data.dict_of_vars)

        # Format responses
        result_data = [response.dict() if hasattr(response, 'dict') else response for response in responses]
        logging.info(f"Processed {len(result_data)} responses")

        return {
            "message": "Image processed successfully",
            # "data": result_data,
            #checking in production 
            "data": responses,
            "status": "success"
        }

    except HTTPException as he:
        logging.warning(f"Client error: {he.detail}")
        raise
    except Exception as e:
        logging.error(f"Processing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Image processing failed. Please check the image format and try again."
        ) from e
