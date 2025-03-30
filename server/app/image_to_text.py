import pytesseract
import io
from PIL import Image
async def text_to_image(bytes):
    try:    
        image = Image.open(io.BytesIO(bytes))
        extracted_text = pytesseract.image_to_string(image)
        extracted_lines = extracted_text.split('\n')
        extracted_lines = [line.strip() for line in extracted_lines if line.strip()]

        return {"lines": extracted_lines}
    except Exception as e:
        return {"error": str(e)}