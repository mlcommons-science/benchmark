import yaml
import re
import sys
import requests
from cloudmesh.common.console import Console
from pprint import pprint
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
    HTTPError,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    TooManyRedirects,
    SSLError,
)
from collections import OrderedDict
import codecs

from field_format_manager import FieldFormatManager
from cloudmesh.common.util import banner

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import html2text  # Import the html2text library for Markdown conversion
import requests  # Import the requests library for direct HTTP requests
from pybtex.database import parse_string  # Import parse_string from pybtex
import textwrap  # Import the textwrap module for line wrapping


def http_error_message(code, url=None) -> str:
    http_errors = {
        # 1xx Informational
        100: "Continue - The server has received the request headers and the client should proceed with the request.",
        101: "Switching Protocols - The server is switching protocols as requested by the client.",

        # 2xx Success
        200: "OK - The request has succeeded.",
        201: "Created - The request has been fulfilled and resulted in a new resource being created.",
        202: "Accepted - The request has been accepted for processing, but the processing has not been completed.",
        204: "No Content - The server successfully processed the request, and is not returning any content.",
        205: "Reset Content - The server successfully processed the request, and requires the requester to reset the document view.",
        206: "Partial Content - The server is delivering only part of the resource due to a range header from the client.",

        # 3xx Redirection
        301: "Moved Permanently - The requested resource has been assigned a new permanent URI.",
        302: "Found (Temporary Redirect) - The requested resource resides temporarily under a different URI.",
        303: "See Other - The response to the request can be found under another URI using a GET method.",
        304: "Not Modified - The requested resource has not been modified since the conditions specified in the client's headers.",
        307: "Temporary Redirect - The requested resource resides temporarily under a different URI.",
        308: "Permanent Redirect - The request and all future requests should be repeated using another URI.",

        # 4xx Client Error
        400: "Bad Request - The server couldn't understand the request due to invalid syntax.",
        401: "Unauthorized - Authentication is required and has failed or has not yet been provided.",
        403: "Forbidden - The server understood the request but refuses to authorize it.",
        404: "Not Found - The requested resource could not be found on the server.",
        405: "Method Not Allowed - The request method is known by the server but is not supported by the target resource.",
        406: "Not Acceptable - The server cannot produce a response matching the list of acceptable values.",
        408: "Request Timeout - The server timed out waiting for the request.",
        409: "Conflict - The request could not be completed due to a conflict with the current state of the resource.",
        410: "Gone - The target resource is no longer available at the origin server and this condition is likely permanent.",
        413: "Payload Too Large - The request entity is larger than limits defined by the server.",
        415: "Unsupported Media Type - The server refuses the request because the payload format is in an unsupported format.",
        416: "Range Not Satisfiable - The client has asked for a portion of the file, but the server cannot supply that portion.",
        418: "I'm a teapot - This is a humorous error, not expected to be implemented by HTTP servers.", # For fun
        422: "Unprocessable Entity - The server understands the content type but was unable to process the contained instructions.",
        429: "Too Many Requests - The user has sent too many requests in a given amount of time (rate limiting).",

        # 5xx Server Error
        500: "Internal Server Error - The server has encountered an unexpected condition.",
        501: "Not Implemented - The server does not support the functionality required to fulfill the request.",
        502: "Bad Gateway - The server received an invalid response from an upstream server.",
        503: "Service Unavailable - The server is not ready to handle the request (often due to maintenance or overload).",
        504: "Gateway Timeout - The server didn’t get a response in time from the upstream server.",
        507: "Insufficient Storage - The server is unable to store the representation needed to complete the request.",
    }

    if code in http_errors:
        explanation = http_errors[code]
    else:
        explanation = "Unknown HTTP status code."

    if url:
        return f"{code}: {explanation} at {url}"
    else:
        return f"{code}: {explanation}"

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
        self.chrome_options.add_argument(
            "--disable-dev-shm-usage"
        )  # Overcomes limited resource problems
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )  # Disables browser control by automation
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )  # Removes the "controlled by automation" infobar
        self.chrome_options.add_experimental_option(
            "useAutomationExtension", False
        )  # Disables automation extension

        # Initialize the driver. This creates a new browser instance.
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # Set the User-Agent to mimic a regular browser
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )

    def _convert_html_to_markdown(self, html_content: str) -> str:
        """
        Converts HTML content to Markdown.

        Args:
            html_content (str): The HTML string to convert.

        Returns:
            str: The converted Markdown string.
        """
        h = html2text.HTML2Text()
        h.ignore_links = False  # Configure based on needs (e.g., True to remove links)
        h.ignore_images = (
            False  # Configure based on needs (e.g., True to remove images)
        )
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
        formatted_bibtex_body = bibtex_content  # Default to raw content if pybtex fails

        try:
            # Use pybtex to parse the BibTeX content
            bib_database = parse_string(bibtex_content, bib_format="bibtex")

            # Convert the BibDatabase object back to a string using pybtex's default serialization
            pybtex_serialized = bib_database.to_string("bibtex")

            # Use textwrap to wrap lines to the specified line_length
            # Split the string into lines, wrap each line, then join them back
            wrapped_lines = []
            for line in pybtex_serialized.splitlines():
                # textwrap.fill handles indentation correctly for wrapped lines
                wrapped_lines.append(
                    textwrap.fill(line, width=line_length, subsequent_indent="    ")
                )  # Add some indent for wrapped lines
            formatted_bibtex_body = "\n".join(wrapped_lines)

        except Exception as e:
            Console.warning(
                f"Could not parse or format BibTeX content with pybtex or textwrap: {e}"
            )
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
                    EC.invisibility_of_element_located(
                        (By.XPATH, "//*[contains(text(), 'Just a moment...')]")
                    )
                )
                print(
                    "Successfully waited for 'Just a moment...' to disappear (if present)."
                )
            except Exception:
                # If the "Just a moment..." element wasn't found or didn't disappear,
                # we'll still try to wait for the body element to be present.
                # This handles cases where the "Just a moment..." isn't the issue,
                # but the page is still loading.
                print(
                    "No 'Just a moment...' element found or it persisted. Waiting for body element."
                )
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("Successfully waited for body element to be present.")

            return self.driver.page_source  # Full HTML of the page
        except Exception as e:
            Console.error(f"fetching page: {e}")
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        try:
            response = requests.get(crossref_url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            raw_bibtex = response.text
            return self._format_bibtex_output(raw_bibtex)  # Format the output
        except requests.exceptions.RequestException as e:
            Console.error(f"fetching BibTeX for DOI '{doi}': {e}")
            return None

    def close(self):
        """
        Closes the WebDriver instance.
        It's important to call this method when you are done with the fetcher
        to release browser resources.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None  # Set to None to indicate it's closed


def fetch_webpage(url: str, headers: dict = None) -> str:
    """
    Accesses a web page at the given URL and returns its content.

    Args:
        url (str): The URL of the web page to access.
        headers (dict, optional): A dictionary of HTTP headers to send with the request.
                                  Defaults to a common browser User-Agent if not provided.

    Returns:
        str: The content of the web page if successful, otherwise an error message.

    Example
        url = "https://pubs.acs.org/doi/10.1021/acscatal.0c04525"
        content = fetch_webpage(url)
        if "Page accessed successfully!" in page_content: # Check if the success message is part of the returned content
            print("\nFirst 500 characters of the page content:")
            print(content[:500])
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    try:
        response = requests.get(url, headers=headers)
        explenation = http_error_message(response.status_code)
        if response.status_code == 200:
            return response.text
        else:
            Console.warning(f"{error_message}")
            return explenatio
    except requests.exceptions.ConnectionError as e:
        error_message = (
            f"Connection Error: Could not connect to the server at '{url}'. "
            f"Please check your internet connection or the URL. Details: {e}"
        )
        Console.error(f"{error_message}")
        return error_message
    except requests.exceptions.Timeout as e:
        error_message = (
            f"Timeout Error: The request to '{url}' timed out. "
            f"The server took too long to respond. Details: {e}"
        )
        Console.error(f"{error_message}")
        return error_message
    except requests.RequestException as e:
        error_message = (
            f"An unexpected Request Error occurred while accessing '{url}'. "
            f"Details: {type(e).__name__}: {e}"
        )
        Console.error(f"{error_message}")
        return error_message


class URLChecker:

    def __init__(self, entries: list, verbose: bool = False, ignore_check=None):
        """
        Initializes the URLchecker with a list of flat dictionaries.
        :param entires: List of dictionaries containing entries with URLs.
        """
        self.entries = entries
        self.verbose = verbose
        if ignore_check is None:
            # read file from source/verified_urls.yaml
            try:
                with codecs.open(
                    "source/verified_urls.yaml", "r", encoding="utf-8"
                ) as f:
                    verified_urls = yaml.safe_load(f)
                self.ignore_check = verified_urls.get("urls", [])
            except FileNotFoundError:
                Console.error(
                    "source/verified_urls.yaml not found. No URLs will be ignored."
                )
                self.ignore_check = []
        else:
            self.ignore_check = ignore_check

    #############################################################################################
    # URL Checking
    #############################################################################################

    def is_url_valid(
        self, url: str, timeout: int = 10
    ) -> (bool, str, int | None):  # Modified to return (bool, explanation, status_code)
        """
        Checks if a given URL is accessible and returns a successful HTTP status code (2xx).
        Returns a tuple: (True if valid, False otherwise), an explanation string, and the HTTP status code (or None if no HTTP error).
        """
        try:
            if url is None or url == "":
                error_msg = "URL is empty or None."
                Console.error(error_msg)
                return False, error_msg, None

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, timeout=timeout, headers=headers)
            status_code = response.status_code

            response.raise_for_status()

            Console.msg(f"URL '{url}' is valid with status code {status_code}.")

            if status_code == 403:
                if url in self.ignore_check:
                    Console.warning(
                        f"URL '{url}' is in the ignore list, skipping further checks."
                    )
                    return True, "URL is in the ignore list", status_code

            if status_code == 403:
                error_msg = f"Access to '{url}' via requests is forbidden (HTTP 403). Trying Chrome"

                # Create an instance of the SeleniumFetcher
                try:
                    fetcher = SeleniumFetcher(
                        headless=True
                    )  # Set to False to see the browser

                    print(f"Attempting to fetch HTML from: {url}")
                    # Fetch HTML content
                    html_content = fetcher.fetch_page_html(url, wait_time=15)
                    if html_content:

                        print(f"Converting fetched HTML to Markdown and printing...")
                        markdown_content = fetcher._convert_html_to_markdown(
                            html_content
                        )
                        print("\nPage content converted to Markdown!")
                        print("--- Full Markdown Content (first 1000 chars) ---")
                        print(
                            markdown_content[:1000]
                        )  # Print first 1000 chars of Markdown for brevity in example
                        print("-----------------------------")
                        print("Markdown content fetched and printed.")
                    else:
                        error_msg = (
                            f"Failed to fetch HTML content from '{url}' via Selenium."
                        )
                        Console.error(error_msg)
                        return False, error_msg, status_code
                except Exception as e:
                    error_msg = f"Failed to access '{url}' via Selenium: {e}"
                    Console.error(error_msg)
                    return False, error_msg, status_code

            return True, "Valid URL", status_code

        except requests.exceptions.MissingSchema:
            error_msg = f"Missing scheme in URL '{url}'. Did you mean to include 'http://' or 'https://'?"
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.InvalidSchema:
            error_msg = (
                f"Invalid URL scheme in '{url}'. Only HTTP and HTTPS are supported."
            )
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.InvalidURL:
            error_msg = f"Invalid URL format: '{url}'. Please check the structure."
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.SSLError as e:
            error_msg = f"SSL error while accessing '{url}': {e}"
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.Timeout:
            error_msg = f"Request to '{url}' timed out after {timeout} seconds."
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.ConnectionError:
            error_msg = f"Could not connect to '{url}'. Check your internet connection or the URL."
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.TooManyRedirects:
            error_msg = f"Too many redirects while trying to access '{url}'."
            Console.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            explanation = http_error_message(status_code, url=url)
            error_msg = f"HTTP Error {status_code} for '{url}'. {explanation}"
            Console.error(error_msg)
            return (
                False,
                explanation,
                status_code,
            )  # Return the explanation and status code
        except requests.exceptions.RequestException as e:
            error_msg = f"A request error occurred for '{url}': {e}"
            Console.error(error_msg)
            return False, error_msg, None
        except Exception as e:
            error_msg = f"An unexpected error occurred for '{url}': {e}"
            Console.error(error_msg)
            return False, error_msg, None

    def check_urls(self, printing_status: bool = True) -> bool:
        """
        Returns whether all the URLs in the manager's YAML files are valid.

        Any field without subfields that ends with "url" is checked.
        The "cite" field's URL is also checked.

        Parameters:
            printing_status (bool): whether to print statuses
        Returns:
            bool: True if all URLs are valid, False otherwise
        """

        issues = []
        valid = []
        checked_urls = (
            {}
        )  # To avoid checking the same URL multiple times, store URL and its validity
        urls_by_name = OrderedDict()

        def error(
            name, url, message, status_code=None
        ):  # Modified to accept status_code
            """
            Helper function to log issues with URLs.
            """
            i = {
                "name": name,
                "url": url,
                "message": message,
                "status_code": status_code,
            }  # Store status_code
            issues.append(i)

        for entry in self.entries:  # Use the flat property directly
            name = entry.get("name")
            if name not in urls_by_name:
                urls_by_name[name] = []
            banner(f"Checking URLs for entry: '{name}'")
            for key, value in entry.items():
                # Handle flat keys with 'url'
                if key.lower().endswith("url"):
                    if isinstance(value, str) and value != "":
                        urls_by_name[name].append(
                            value
                        )  # Store the URL under the entry name
                # Handle BibTeX citation strings which might be directly in a 'cite' key,
                # or if 'cite' key can contain a list of strings, each being a bibtex entry.
                # Assuming 'cite' itself is a key in the flattened dict.
                elif key == "cite":
                    if isinstance(
                        value, str
                    ):  # 'cite' field itself is a string with BibTeX
                        urls_by_name[name].extend(
                            re.findall(r"url\s*=\s*\{(.*?)\}", value)
                        )
                    elif isinstance(
                        value, list
                    ):  # 'cite' field is a list of BibTeX strings
                        for bib_string in value:
                            if isinstance(bib_string, str):
                                urls_by_name[name].extend(
                                    re.findall(r"url\s*=\s*\{(.*?)\}", bib_string)
                                )

        pprint(urls_by_name)  # Debug print to see collected URLs

        for name, urls in urls_by_name.items():
            print()
            banner(f"Checking URLs for entry '{name}'...")

            if not urls:
                if printing_status:
                    msg = f"No URLs found for entry '{name}'"
                    Console.warning(msg)
                    error(name, None, msg)
                continue

            for url in urls:
                Console.msg(f"  Checking URL: '{url}'")
                # Check if the URL has already been checked
                if url in checked_urls:
                    if checked_urls[url]["is_valid"]:
                        Console.warning(
                            f"URL '{url}' duplicated, already checked and is valid."
                        )
                    else:
                        Console.warning(
                            f"URL '{url}' duplicated, already checked and found to be invalid: {checked_urls[url]['explanation']}"
                        )
                    continue  # Skip re-checking if already processed

                is_valid, explanation, status_code = self.is_url_valid(
                    url
                )  # Capture status_code
                checked_urls[url] = {
                    "is_valid": is_valid,
                    "explanation": explanation,
                    "status_code": status_code,
                }  # Store status_code

                if is_valid:
                    valid.append(url)
                else:
                    msg = f"Invalid URL: '{url}' for entry '{name}' - {explanation}"  # Include explanation here
                    Console.error(msg)
                    error(
                        name, url, explanation, status_code
                    )  # Pass the status_code to the error function

        print()
        banner("Summary of URL check errors")
        print()

        all_urls_valid = not issues

        if all_urls_valid:
            Console.msg("All URLs checked are valid.")
        else:
            for issue in issues:
                error_detail = ""
                if issue["status_code"]:
                    # Use explain_http_error to get the detailed message for the summary
                    Console.ok(f"{issue['status_code']} - {issue['url']}")
                    error_detail = http_error_message(
                        issue["status_code"], issue["url"]
                    )
                else:
                    error_detail = issue[
                        "message"
                    ]  # For non-HTTP errors, use the stored message

                Console.error(
                    f"Entry '{issue['name']}' has an issue with URL '{issue['url']}'"
                    f"{f' (Status: {issue["status_code"]})' if issue['status_code'] else ''}: {error_detail}"
                )
            print()
            count = len(issues)
            Console.info(f"At least {count} URLs had issues.")
            print("#" * 79)
            Console.info(
                "The sumary does not include duplicated URL errors, only unique issues."
            )
            Console.info("The summary does not unclude all malformed URLS")

        return all_urls_valid


# Example usage
if __name__ == "__main__":
    url = "https://pubs.acs.org/doi/10.1021/acscatal.0c04525"
    doi = "10.1021/acscatal.0c04525"

    # Create an instance of the SeleniumFetcher
    fetcher = SeleniumFetcher(headless=True)  # Set to False to see the browser

    try:
        print(f"Attempting to fetch HTML from: {url}")
        # Fetch HTML content
        html_content = fetcher.fetch_page_html(url, wait_time=15)
        if html_content:
            print("\nPage accessed successfully (HTML)!")
            print("--- Full HTML Content (first 1000 chars) ---")
            print(
                html_content[:1000]
            )  # Print first 1000 chars of HTML for brevity in example
            print("-------------------------")
            print("HTML content fetched and printed.")

            print("\n" + "=" * 50 + "\n")  # Separator

            # Convert HTML to Markdown and print
            print(f"Converting fetched HTML to Markdown and printing...")
            markdown_content = fetcher._convert_html_to_markdown(html_content)
            print("\nPage content converted to Markdown!")
            print("--- Full Markdown Content (first 1000 chars) ---")
            print(
                markdown_content[:1000]
            )  # Print first 1000 chars of Markdown for brevity in example
            print("-----------------------------")
            print("Markdown content fetched and printed.")

            print("\n" + "=" * 50 + "\n")  # Separator

            # Fetch BibTeX from DOI (now includes formatting)
            print(f"Attempting to fetch BibTeX for DOI: {doi}")
            bibtex_content = fetcher.fetch_bibtex_from_doi(doi)
            if bibtex_content:
                print(bibtex_content)  # Print the already formatted content
            else:
                print(f"\nFailed to fetch BibTeX for DOI: {doi}")

        else:
            print("\nFailed to fetch the page (HTML).")

    finally:
        # Ensure the driver is closed even if an error occurs
        print("Closing Selenium WebDriver.")
        fetcher.close()
