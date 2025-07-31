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
from url_checker_chrome import SeleniumFetcher
from cloudmesh.common.util import banner



class URLChecker:

    def __init__(self, entries: list, verbose: bool = False):
        """
        Initializes the URLchecker with a list of flat dictionaries.
        :param entires: List of dictionaries containing entries with URLs.
        """
        self.entries = entries
        self.verbose = verbose

    #############################################################################################
    # URL Checking
    #############################################################################################

    def explain_http_error(self, code, url=None, with_url: bool = False) -> str:
        http_errors = {
            400: "Bad Request - The server couldn't understand the request due to invalid syntax.",
            401: "Unauthorized - Authentication is required and has failed or has not yet been provided.",
            403: "Forbidden - The server understood the request but refuses to authorize it.",
            404: "Not Found - The requested resource could not be found on the server.",
            405: "Method Not Allowed- The request method is known by the server but is not supported by the target resource.",
            408: "Request Timeout - The server timed out waiting for the request.",
            429: "Too Many Requests - The user has sent too many requests in a given amount of time (rate limiting).",
            500: "Internal Server Error - The server has encountered a situation it doesn't know how to handle.",
            502: "Bad Gateway - The server received an invalid response from the upstream server.",
            503: "Service Unavailable - The server is not ready to handle the request (often due to maintenance or overload).",
            504: "Gateway Timeout - The server didn’t get a response in time from the upstream server.",
        }

        explanation = http_errors.get(
            code, "Unknown error code - not a standard HTTP error."
        )

        if url and not with_url:
            return f"{explanation}: {code} at {url}"
        else:
            return f"{explanation}"

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
            explanation = self.explain_http_error(status_code, url)
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

        print("\n", "#" * 79)
        print("# Summary of URL check errors")
        print("#", "#" * 79)

        all_urls_valid = not issues

        if all_urls_valid:
            Console.msg("All URLs checked are valid.")
        else:
            for issue in issues:
                error_detail = ""
                if issue["status_code"]:
                    # Use explain_http_error to get the detailed message for the summary
                    error_detail = self.explain_http_error(
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
