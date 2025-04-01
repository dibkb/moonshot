import random
from fastapi import FastAPI,WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import time
from playwright.async_api import async_playwright, Playwright
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from .page import get_page_text
from .get_text import get_clean_text
from .execute_cick import execute_click
from .actions.click import extract_click_elements
from .execute_search import execute_search
from .actions.search import extract_fill_click
from .actions.fill import extract_fill_elements
from .generate import generate_plan
from .extract import extract_elements
from .image_to_text import text_to_image
from .execute_fill import execute_fill
from .task.update import send_update
from playwright_stealth import stealth_async
import uuid
import asyncio
from pydantic import BaseModel


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



# Global dictionary mapping task IDs to their asyncio.Queue
task_queues = {}

class TaskRequest(BaseModel):
    query: str

@app.post("/tasks")
async def create_task(task: TaskRequest, background_tasks: BackgroundTasks):
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    # Create an asyncio queue for this task and store it in the global dictionary
    task_queue = asyncio.Queue()
    task_queues[task_id] = task_queue
    # Launch the background automation task
    background_tasks.add_task(run_browser_automation, task_id, task.query)
    # Return the task ID to the client
    return {"task_id": task_id}

async def run_browser_automation(task_id: str, query: str):

    global browser
    if not browser:
        return;
    
    queue = task_queues.get(task_id)
    if not queue:
        return
        
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
            update = f"Update : Processing step '{step}'..."
            await send_update(queue,update)
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
                content = await get_clean_text(page)
                print("\n")
                print("content",content)
                print("\n")

                # fill-click
                if action_type == "click":
                    click_action = extract_click_elements(element_metadata,description)
    
                    await execute_click(page,click_action)
                if action_type == "fill":
                    fill_action = extract_fill_elements(element_metadata,description,objective)
                    await execute_fill(page,fill_action,params)
                if action_type == "fill-click":
                    fill_click_action = extract_fill_click(element_metadata,description,objective)
                    await execute_search(page,fill_click_action,params)
            elif step['type'] == "EXTRACT":
                # validate not captcha page
                await page.wait_for_load_state('networkidle')
                screenshot_bytes = await page.screenshot()
                content = await text_to_image(screenshot_bytes)
                text = await page.inner_text("body")
                print("\n")
                print("text",text)
                print("\n")
                pass
        # await page.close()
        await queue.put("Task Completed")
    except Exception as e:
        print(e)

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """
    WebSocket endpoint to subscribe to task updates.
    It listens to the corresponding asyncio.Queue and forwards messages to the client.
    """
    await websocket.accept()
    queue = task_queues.get(task_id)
    if not queue:
        await websocket.send_text("Invalid task ID")
        await websocket.close()
        return

    try:
        while True:
            message = await queue.get()
            await websocket.send_text(message)

            if message == "Task Completed":
                break
    except WebSocketDisconnect:
        pass
    finally:

        task_queues.pop(task_id, None)

    


    


