import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import time
import os
from playwright.async_api import async_playwright, Playwright
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from .execute_cick import execute_click
from .actions.click import extract_click_elements
from .execute_search import execute_search
from .actions.search import extract_fill_click
from .actions.fill import extract_fill_elements
from .generate import generate_plan
from .extract import extract_elements
from .image_to_text import text_to_image
from .execute_fill import execute_fill
from playwright_stealth import stealth_async
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
    browser = await playwright_instance.chromium.launch(channel="msedge",headless=False)
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
        # Define random viewport dimensions and common headers
        viewport_width = random.randint(1024, 1920)
        viewport_height = random.randint(768, 1080)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

        # Create new page with enhanced configuration
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height},
            user_agent=headers['User-Agent'],
            ignore_https_errors=True,
            extra_http_headers=headers,
            locale='en-US',
            timezone_id='America/New_York',
            geolocation={'latitude': 40.730610, 'longitude': -73.935242},  # New York coordinates
            permissions=['geolocation']
        )
        
        page = await context.new_page()
        await stealth_async(page)
        
        plan = generate_plan(query)
        # Interact with login form
        for step in plan['steps']:
            print(step)
            print('\n')
            # await page.wait_for_load_state('networkidle')
            if step['type'] == "NAVIGATE":
                await page.goto(step['params']['url'])
            elif step['type'] == "INTERACT":
                element_metadata = await extract_elements(page)
                # Capture screenshot and page text
                # screenshot_bytes = await page.screenshot()
                # validate not captcha page
                # content = await text_to_image(screenshot_bytes)
                objective = step['objective']
                params = step['params']
                action_type = params['action_type']
                description = params['description']

                # print("\n")
                # print("element_metadata",element_metadata)
                # print("\n")

                # fill-click
                if action_type == "click":
                    click_action = extract_click_elements(element_metadata,description)
    
                    await execute_click(page,click_action)
                if action_type == "fill":
                    fill_action = extract_fill_elements(element_metadata,description,objective)
                    await execute_fill(page,fill_action,params)
                if action_type == "fill-click":
                    print("fill-click")
                    fill_click_action = extract_fill_click(element_metadata,description,objective)
                    print(fill_click_action)
                    print('\n')
                    await execute_search(page,fill_click_action,params)
            elif step['type'] == "EXTRACT":
                pass
        # await page.close()
        return JSONResponse(content=plan)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


