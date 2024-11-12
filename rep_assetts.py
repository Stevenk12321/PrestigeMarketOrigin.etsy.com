from playwright.sync_api import sync_playwright
import random
import time

# Function to set up a random user-agent to avoid detection
def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/91.0.864.64',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]
    return random.choice(user_agents)

# Function to bypass CAPTCHA by using proxy and headless browsing
def bypass_captcha(page):
    # You can rotate proxies and user agents to reduce CAPTCHA chances
    user_agent = get_random_user_agent()
    print(f"Using User-Agent: {user_agent}")
    
    # Set the user agent for the browser context (not the page directly)
    context = page.context
    context.set_user_agent(user_agent)
    
    # Example: Wait for network idle (no more requests being made)
    page.wait_for_load_state('networkidle', timeout=60000)  # 60 seconds

    # If CAPTCHA still appears, you can use services like 2Captcha or Anti-Captcha to solve the CAPTCHA
    # However, this part would require API calls to those services, which are out of scope for a basic script.

# Main function that replicates the webpage and interacts with it
def replicate_website():
    with sync_playwright() as p:
        # Launch Chromium browser with headless mode set to False for debugging
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()  # Create a new browser context to set the user agent
        page = context.new_page()  # Create a new page within the context

        # Open the target website
        page.goto("https://www.etsy.com/shop/prestigemarketorigin/?etsrc=sdt")  # Replace with the URL you want to replicate
        
        # Wait for the page to fully load before interaction
        page.wait_for_load_state('load', timeout=60000)  # Wait up to 60 seconds

        # Bypass CAPTCHA if it appears
        bypass_captcha(page)

        # Example: Interact with a button on the page
        try:
            # Wait for the submit button to be visible and enabled
            page.wait_for_selector('button#submit', state='visible', timeout=60000)
            page.wait_for_selector('button#submit', state='enabled', timeout=60000)
            
            # Click the submit button
            page.click('button#submit')
            print("Button clicked successfully.")
        except Exception as e:
            print(f"Error while clicking the button: {str(e)}")

        # Wait for a while to observe changes after the click (if needed)
        time.sleep(5)

        # Optionally, take a screenshot of the page after interaction
        page.screenshot(path="replicated_page.png")

        # Save the page HTML to a file (if you want to replicate it in HTML form)
        page_content = page.content()
        with open("replicated_page.html", "w", encoding="utf-8") as file:
            file.write(page_content)
        
        # Close the browser
        browser.close()

if __name__ == "__main__":
    replicate_website()

