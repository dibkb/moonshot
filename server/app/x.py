async def generate_stream():
        try:
            while browser:  # Simply check if browser reference exists
                try:
                    page = await browser.new_page()

                    async def handle_url_change(frame):
                        screenshot_bytes = await page.screenshot()
                        page_text = await text_to_image(screenshot_bytes)
                        update = {
                            "url": page.url,
                            "timestamp": time.time(),
                            "page_text": page_text
                        }
                        print(update)
                        yield f"data: {jsonable_encoder(update)}\n\n"


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
                    
                    # submit_button = await page.query_selector('input[type="submit"][value="Google Search"]')
                    # if submit_button:
                    #     async with page.expect_navigation():
                    #         await submit_button.click()

                    # 
                    # Keep connection alive with heartbeat
                    # while True:
                    #     await asyncio.sleep(30)  # Heartbeat every 30 seconds
                    #     yield "data: heartbeat\n\n"

                except Exception as e:
                    yield f"data: {{'error': '{str(e)}'}}\n\n"
                    if(str(e) == "Page.goto: Target page, context or browser has been closed"):
                        await browser.close()
                finally:
                    try:
                        await page.close()
                    except:
                        pass  # Ignore errors if page can't be closed
        finally:
            # Yield final message when stream ends
            yield "data: {\"status\": \"disconnected\"}\n\n"