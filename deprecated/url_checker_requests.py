import requests


def access_webpage(url: str, headers: dict = None) -> str:
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
        content = access_webpage(url)
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

        if response.status_code == 200:
            print("Page accessed successfully!")
            return response.text
        else:
            # Using a dictionary to emulate a switch statement for status codes
            status_code_messages = {
                400: (
                    f"Bad Request (400): The server could not understand the request for '{url}'. "
                    "This might indicate malformed syntax or invalid parameters."
                ),
                401: (
                    f"Unauthorized (401): Authentication is required for '{url}' and has failed or "
                    "has not yet been provided."
                ),
                403: (
                    f"Access forbidden (403): The server refused the request for '{url}'. "
                    "This might be due to robot detection, IP blocking, or missing authentication."
                ),
                404: (
                    f"Not Found (404): The requested URL '{url}' was not found on the server. "
                    "Please check the URL for typos."
                ),
                500: (
                    f"Internal Server Error (500): The server encountered an unexpected condition "
                    f"which prevented it from fulfilling the request for '{url}'."
                ),
                503: (
                    f"Service Unavailable (503): The server for '{url}' is currently unable to handle "
                    "the request due to temporary overloading or maintenance of the server."
                ),
            }

            # Get the specific message for the status code, or a generic one if not found
            error_message = status_code_messages.get(
                response.status_code,
                f"Request returned unexpected status code: {response.status_code} ({response.reason}) "
                f"for URL '{url}'. No specific handler for this code.",
            )
            print(f"Warning: {error_message}")
            return error_message
    except requests.exceptions.ConnectionError as e:
        error_message = (
            f"Connection Error: Could not connect to the server at '{url}'. "
            f"Please check your internet connection or the URL. Details: {e}"
        )
        print(f"Error: {error_message}")
        return error_message
    except requests.exceptions.Timeout as e:
        error_message = (
            f"Timeout Error: The request to '{url}' timed out. "
            f"The server took too long to respond. Details: {e}"
        )
        print(f"Error: {error_message}")
        return error_message
    except requests.RequestException as e:
        error_message = (
            f"An unexpected Request Error occurred while accessing '{url}'. "
            f"Details: {type(e).__name__}: {e}"
        )
        print(f"Error: {error_message}")
        return error_message
