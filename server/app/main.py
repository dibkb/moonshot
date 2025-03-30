from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import time
import os
from playwright.async_api import async_playwright, Playwright
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from .run import run
from .page import get_page_text
from .image_to_text import text_to_image
import base64
import asyncio

app = FastAPI(
    title="FastAPI Demo",
    description="A FastAPI application with Docker and Poetry",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    global browser, playwright_instance
    playwright_instance = await async_playwright().start()
    # Launch the browser in headed mode (headless=False)
    browser = await playwright_instance.chromium.launch(channel="chrome",headless=False)
    # Optionally, create a default page or context here if needed.
    print("Browser started and will remain open until server shutdown.")


@app.on_event("shutdown")
async def shutdown():
    global browser, playwright_instance
    if browser:
        await browser.close()
    if playwright_instance:
        await playwright_instance.stop()
    print("Browser and Playwright have been closed.")

@app.get("/")
async def root():
    return {"Moonshot Server is running 🚀"}

@app.get("/health")
async def health_check():
    return f"Healthy {time.time()}"


# @app.get('/text-to-image')
# async def text_to_image():
#     try:
#         screenshot_path = './app/ss/1.png'
#         print(os.getcwd())
#         if not os.path.exists(screenshot_path):
#             return {"error": "Screenshot file not found"}
            
#         image = Image.open(screenshot_path)
#         extracted_text = pytesseract.image_to_string(image)
#         extracted_lines = extracted_text.split('\n')
#         extracted_lines = [line.strip() for line in extracted_lines if line.strip()]

#         return {"lines": extracted_lines}
#     except Exception as e:
#         return {"error": str(e)}
    
@app.get("/visual-elements")
async def capture_visual_context():
    global browser
    if not browser:
        return {"error": "Browser not available."}
    
    async def generate_stream():
        while True:  # Continuous stream
            try:
                page = await browser.new_page()
                current_url = page.url

                async def handle_url_change(frame):
                    nonlocal current_url
                    new_url = page.url
                    screenshot_bytes = await page.screenshot()
                    page_text = await text_to_image(screenshot_bytes)
                    if new_url != current_url:
                        update = {
                            "from": current_url,
                            "to": new_url,
                            "timestamp": time.time(),
                            "page_text": page_text
                        }
                        yield f"data: {jsonable_encoder(update)}\n\n"
                        current_url = new_url

                # Set up URL change listener
                page.on("framenavigated", handle_url_change)

                await page.goto("https://www.google.com")
                elements = await page.query_selector_all('input,button,textarea')
                
                element_metadata = []
                for element in elements:
                    box = await element.bounding_box()
                    if box:
                        metadata = {
                            "selector": await element.get_attribute("id") or await element.get_attribute("name"),
                            "type": await element.get_attribute("type"),
                            "value": await element.get_attribute("value"),
                            'title': await element.get_attribute('title'),
                            "tag": await element.evaluate('element => element.tagName.toLowerCase()'),
                            "position": {
                                "x": box["x"],
                                "y": box["y"],
                                "width": box["width"],
                                "height": box["height"]
                            },
                            "text": await element.inner_text()
                        }
                        element_metadata.append(metadata)

                yield f"data: {jsonable_encoder({'elements': element_metadata})}\n\n"
                # Rest of the interaction logic
                textarea = await page.query_selector('textarea')
                if textarea:
                    await textarea.fill("hello world")
                
                submit_button = await page.query_selector('input[type="submit"][value="Google Search"]')
                if submit_button:
                    async with page.expect_navigation():
                        await submit_button.click()

                await page.wait_for_load_state('networkidle')
                # Keep connection alive with heartbeat
                while True:
                    await asyncio.sleep(30)  # Heartbeat every 30 seconds
                    yield "data: heartbeat\n\n"

            except Exception as e:
                yield f"data: {{'error': '{str(e)}'}}\n\n"
                await asyncio.sleep(5)  # Wait before retry
                continue
            finally:
                await page.close()

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )
    