import asyncio
import os
from playwright.async_api import async_playwright

async def generate_pdf():
    # File paths
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(curr_dir, "JavierSavidTeixeira_CV.html")
    pdf_file = os.path.join(curr_dir, "JavierSavidTeixeira_CV.pdf")
    
    # Ensure the HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found.")
        return

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load HTML file
        # Using file:/// protocol for local file access
        await page.goto(f"file:///{html_file.replace(os.sep, '/')}")
        
        # Wait for fonts and styles to load
        await page.wait_for_load_state("networkidle")
        
        # Generate PDF
        # display_header_footer=False ensures no data in the margins
        # print_background=True ensures colors/gradients are preserved
        await page.pdf(
            path=pdf_file,
            format="A4",
            print_background=True,
            display_header_footer=False,
            margin={"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"}
        )
        
        await browser.close()
        print(f"Successfully generated: {pdf_file}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
