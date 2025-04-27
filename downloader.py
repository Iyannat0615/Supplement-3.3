import requests
import threading
import sys
import os


#Sequential download time: 3.330415964126587 seconds
#Multithreaded download time: 0.32100820541381836 seconds
# Based on test runs on my computer.

def download_file(url, filename):
    """
    Downloads a file from a given URL and saves it to the specified filename.

    Parameters:
    - url (str): The URL to download the file from.
    - filename (str): The name of the file to save the downloaded content as.

    Returns:
    - bool: True if the file was downloaded successfully, False otherwise.

    Raises:
    - requests.exceptions.RequestException: If any error occurs during the download (e.g., invalid URL).
    """
    try:
        # Sending a GET request to the URL to fetch the file, stream=True ensures the content is downloaded in chunks.
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 OK.

        # Open the file in write-binary mode to save the content as it is being downloaded.
        with open(filename, "wb") as file:
            # Iterating over the content in chunks of 8192 bytes to avoid memory overload for large files.
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Print a success message with the filename upon successful download.
        print(f"✅ Downloaded: {filename}")
        return True

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the download process and print an error message.
        print(f"❌ Error downloading {url}: {e}")
        return False

def download_from_url(url):
    """
    Extracts the filename from the URL and invokes the `download_file` function to download the file.

    Parameters:
    - url (str): The URL to download the file from.

    Returns:
    - None
    """
    # Extracts the base filename from the URL using os.path.basename.
    # If the URL doesn't contain a valid filename, a default name 'downloaded_file' is used.
    filename = os.path.basename(url) or "downloaded_file"
    # Calling the `download_file` function to handle the download.
    download_file(url, filename)

if __name__ == "__main__":
    """
    Main execution point of the script. Accepts multiple URLs from command-line arguments and 
    initiates the download of each file using multiple threads.

    Parameters:
    - sys.argv: A list of command-line arguments where each argument is expected to be a URL.

    Returns:
    - None
    """
    # Get the URLs from the command-line arguments passed to the script.
    urls = sys.argv[1:]

    # Check if no URLs were provided.
    if not urls:
        print("\n⚠️  No URLs provided.\n")
        print("Usage: python downloader.py <url1> <url2> ...")
        sys.exit(1)  # Exit the script with a non-zero status to indicate failure.

    # List to hold all the threads.
    threads = []

    # Iterate over each URL to create a thread for downloading the file.
    for url in urls:
        # Create a new thread for each download task.
        thread = threading.Thread(target=download_from_url, args=(url,))
        # Add the thread to the threads list.
        threads.append(thread)
        # Start the thread to download the file.
        thread.start()

    # Wait for all threads to finish before exiting.
    for thread in threads:
        thread.join()

    # Once all downloads are complete, print a success message.
    print("\n🎉 All downloads complete.")
