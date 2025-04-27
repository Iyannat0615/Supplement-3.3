import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Replace with actual file URLs
files = [
    "https://example.com/file1.jpg",
    "https://example.com/file2.jpg",
    "https://example.com/file3.jpg",
    "https://example.com/file4.jpg",
    "https://example.com/file5.jpg"
]

# Sequential download function
def download_sequential(files):
    for file in files:
        response = requests.get(file)
        with open(file.split('/')[-1], 'wb') as f:
            f.write(response.content)

# Multithreaded download function
def download_multithreaded(files):
    def download_file(file):
        response = requests.get(file)
        with open(file.split('/')[-1], 'wb') as f:
            f.write(response.content)
    
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, files)

# Measure time for sequential download
start_time = time.time()
download_sequential(files)
sequential_time = time.time() - start_time

# Measure time for multithreaded download
start_time = time.time()
download_multithreaded(files)
multithreaded_time = time.time() - start_time

# Output times
print(f"Sequential download time: {sequential_time} seconds")
print(f"Multithreaded download time: {multithreaded_time} seconds")
