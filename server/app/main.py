from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import time
import os
from playwright.async_api import async_playwright, Playwright
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from .execute_search import execute_search
from .actions.search import extract_search_elements
from .generate import generate_plan
from .extract import extract_elements
from .image_to_text import text_to_image

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
async def capture_visual_context(query: str):
    global browser
    if not browser:
        return JSONResponse(content={"error": "Browser not available."})
        
    try:
        # page = await browser.new_page()
        # links = ['https://www.amazon.in/','https://www.google.com/','https://www.youtube.com/']
        # await page.goto(links[2])
            
        # # Capture elements
        
        # response_data = {
        #     "url": page.url,
        #     "timestamp": time.time(),
        #     "content": content,
        #     "elements": element_metadata
        # }
        plan = generate_plan(query)
        page = await browser.new_page()
        for step in plan['steps']:
            # await page.wait_for_load_state('networkidle')
            if step['type'] == "NAVIGATE":
                await page.goto(step['context']['url'])
            elif step['type'] == "INTERACT":
                element_metadata = await extract_elements(page)
                # Capture screenshot and page text
                screenshot_bytes = await page.screenshot()
                # validate not captcha page
                content = await text_to_image(screenshot_bytes)
                objective = step['objective']
                context = step['context']
                search_action = extract_search_elements(element_metadata)
                await execute_search(page,search_action,context)
            elif step['type'] == "EXTRACT":
                pass
        # await page.close()
        return JSONResponse(content=plan)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    