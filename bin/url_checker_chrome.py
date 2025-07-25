from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import html2text # Import the html2text library for Markdown conversion
import requests # Import the requests library for direct HTTP requests
from pybtex.database import parse_string # Import parse_string from pybtex
import textwrap # Import the textwrap module for line wrapping

class SeleniumFetcher:
    """
    A class to fetch HTML content of webpages using Selenium WebDriver.
    Includes improvements to handle anti-bot detections like "Just a moment...".
    """

    def __init__(self, headless: bool = True):
        """
        Initializes the SeleniumFetcher with Chrome WebDriver options.

        Args:
            headless (bool): Whether to run Chrome in headless mode (default: True).
        """
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")

        # Common arguments to make Selenium less detectable
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Disables browser control by automation
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Removes the "controlled by automation" infobar
        self.chrome_options.add_experimental_option('useAutomationExtension', False) # Disables automation extension

        # Initialize the driver. This creates a new browser instance.
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # Set the User-Agent to mimic a regular browser
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})

    def _convert_html_to_markdown(self, html_content: str) -> str:
        """
        Converts HTML content to Markdown.

        Args:
            html_content (str): The HTML string to convert.

        Returns:
            str: The converted Markdown string.
        """
        h = html2text.HTML2Text()
        h.ignore_links = False # Configure based on needs (e.g., True to remove links)
        h.ignore_images = False # Configure based on needs (e.g., True to remove images)
        # You can add more configurations here, e.g., h.body_width = 0 for no line wrapping
        markdown_content = h.handle(html_content)
        return markdown_content

    def _format_bibtex_output(self, bibtex_content: str, line_length: int = 80) -> str:
        """
        Formats the BibTeX string with a nice header and footer, and wraps lines.
        Uses pybtex for parsing/re-serialization and textwrap for line length control.

        Args:
            bibtex_content (str): The raw BibTeX string.
            line_length (int): The maximum desired line length for the BibTeX entries.

        Returns:
            str: The formatted BibTeX string (with headers/footers and wrapped lines).
        """
        formatted_bibtex_body = bibtex_content # Default to raw content if pybtex fails

        try:
            # Use pybtex to parse the BibTeX content
            bib_database = parse_string(bibtex_content, bib_format='bibtex')

            # Convert the BibDatabase object back to a string using pybtex's default serialization
            pybtex_serialized = bib_database.to_string('bibtex')

            # Use textwrap to wrap lines to the specified line_length
            # Split the string into lines, wrap each line, then join them back
            wrapped_lines = []
            for line in pybtex_serialized.splitlines():
                # textwrap.fill handles indentation correctly for wrapped lines
                wrapped_lines.append(textwrap.fill(line, width=line_length, subsequent_indent='    ')) # Add some indent for wrapped lines
            formatted_bibtex_body = "\n".join(wrapped_lines)

        except Exception as e:
            print(f"Warning: Could not parse or format BibTeX content with pybtex or textwrap: {e}")
            # In case of parsing/formatting error, the original raw_bibtex will be used.

        header = "=" * 10 + " BIBTEX CITATION " + "=" * 10
        # Adjust footer length to match header
        footer_length = len(header)
        footer = "=" * footer_length
        return f"\n{header}\n{formatted_bibtex_body}\n{footer}\n"

    def fetch_page_html(self, url: str, wait_time: int = 10) -> str | None:
        """
        Fetches the HTML content of a webpage using the initialized Selenium WebDriver.
        Includes a wait mechanism to handle dynamic content or anti-bot pages.

        Args:
            url (str): The URL of the webpage to fetch.
            wait_time (int): Maximum time in seconds to wait for the page to load
                             or for specific elements to be present.

        Returns:
            str: The HTML content of the page (or None if failed).
        """
        try:
            self.driver.get(url)

            # Add a short, static sleep first, sometimes this helps with initial anti-bot checks
            time.sleep(2)

            # Wait until the "Just a moment..." text is no longer present,
            # or until a common page element (e.g., body) is loaded.
            # We'll try to wait for the absence of the "Just a moment..." text
            # or for the presence of the <body> tag, assuming it's the main content.
            try:
                # Wait for the element containing "Just a moment..." to disappear
                WebDriverWait(self.driver, wait_time).until(
                    EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Just a moment...')]"))
                )
                print("Successfully waited for 'Just a moment...' to disappear (if present).")
            except Exception:
                # If the "Just a moment..." element wasn't found or didn't disappear,
                # we'll still try to wait for the body element to be present.
                # This handles cases where the "Just a moment..." isn't the issue,
                # but the page is still loading.
                print("No 'Just a moment...' element found or it persisted. Waiting for body element.")
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("Successfully waited for body element to be present.")

            return self.driver.page_source  # Full HTML of the page
        except Exception as e:
            print(f"Error fetching page: {e}")
            return None

    def fetch_bibtex_from_doi(self, doi: str) -> str | None:
        """
        Fetches BibTeX citation for a given DOI using CrossRef content negotiation.
        This method uses direct HTTP requests (requests library) as it's more suitable
        for fetching specific content types like BibTeX than a full browser rendering.

        Args:
            doi (str): The Digital Object Identifier (e.g., "10.1021/acscatal.0c04525").

        Returns:
            str: The BibTeX string, formatted with a header and footer, or None if fetching failed.
        """
        # CrossRef's content negotiation endpoint
        crossref_url = f"https://doi.org/{doi}"
        headers = {
            "Accept": "application/x-bibtex",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(crossref_url, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            raw_bibtex = response.text
            return self._format_bibtex_output(raw_bibtex) # Format the output
        except requests.exceptions.RequestException as e:
            print(f"Error fetching BibTeX for DOI '{doi}': {e}")
            return None

    def close(self):
        """
        Closes the WebDriver instance.
        It's important to call this method when you are done with the fetcher
        to release browser resources.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None # Set to None to indicate it's closed

# Example usage
if __name__ == "__main__":
    url = "https://pubs.acs.org/doi/10.1021/acscatal.0c04525"
    doi = "10.1021/acscatal.0c04525"

    # Create an instance of the SeleniumFetcher
    fetcher = SeleniumFetcher(headless=True) # Set to False to see the browser

    try:
        print(f"Attempting to fetch HTML from: {url}")
        # Fetch HTML content
        html_content = fetcher.fetch_page_html(url, wait_time=15)
        if html_content:
            print("\nPage accessed successfully (HTML)!")
            print("--- Full HTML Content (first 1000 chars) ---")
            print(html_content[:1000]) # Print first 1000 chars of HTML for brevity in example
            print("-------------------------")
            print("HTML content fetched and printed.")

            print("\n" + "="*50 + "\n") # Separator

            # Convert HTML to Markdown and print
            print(f"Converting fetched HTML to Markdown and printing...")
            markdown_content = fetcher._convert_html_to_markdown(html_content)
            print("\nPage content converted to Markdown!")
            print("--- Full Markdown Content (first 1000 chars) ---")
            print(markdown_content[:1000]) # Print first 1000 chars of Markdown for brevity in example
            print("-----------------------------")
            print("Markdown content fetched and printed.")

            print("\n" + "="*50 + "\n") # Separator

            # Fetch BibTeX from DOI (now includes formatting)
            print(f"Attempting to fetch BibTeX for DOI: {doi}")
            bibtex_content = fetcher.fetch_bibtex_from_doi(doi)
            if bibtex_content:
                print(bibtex_content) # Print the already formatted content
            else:
                print(f"\nFailed to fetch BibTeX for DOI: {doi}")

        else:
            print("\nFailed to fetch the page (HTML).")

    finally:
        # Ensure the driver is closed even if an error occurs
        print("Closing Selenium WebDriver.")
        fetcher.close()

