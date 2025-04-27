import time
import unittest
import threading
import os
from downloader import download_file  # Make sure downloader.py is in the same directory or installed

class TestDownloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up test data once before all tests are run. This method will be executed only once 
        before any of the test methods are run.

        It initializes:
        - `TEST_URLS`: A list of URLs to download files from.
        - `TEST_FILENAMES`: Corresponding list of filenames where the files should be saved.
        """
        cls.TEST_URLS = [
            "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
            "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
            "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
            "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
            "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif",
        ]
        cls.TEST_FILENAMES = [
            "file1.gif", "file2.gif", "file3.gif", "file4.gif", "file5.gif"
        ]

    def tearDown(self):
        """
        Clean up downloaded files after each test.

        This method will be executed after each test method.
        It removes the files downloaded during the test to avoid interference between tests.
        """
        for filename in self.TEST_FILENAMES:
            if os.path.exists(filename):
                os.remove(filename)

    def test_sequential_download(self):
        """
        Test downloading files sequentially.

        This test checks the download time when files are downloaded one after the other.
        It measures the time taken to download each file in sequence.
        """
        start_time = time.perf_counter()  # Start the timer
        for url, filename in zip(self.TEST_URLS, self.TEST_FILENAMES):
            # Download each file sequentially
            success = download_file(url, filename)
            self.assertTrue(success, f"Failed to download {url}")  # Ensure the download was successful
        end_time = time.perf_counter()  # End the timer

        # Calculate and print the total download duration
        duration = end_time - start_time
        print(f"Sequential download time: {duration:.4f} seconds")

    def test_multithreaded_download(self):
        """
        Test downloading files using multithreading.

        This test checks the download time when multiple files are downloaded concurrently 
        using threads. Each download runs in a separate thread to allow parallelism.
        """
        start_time = time.perf_counter()  # Start the timer
        threads = []  # List to hold the threads
        for url, filename in zip(self.TEST_URLS, self.TEST_FILENAMES):
            # Create a new thread for each file download
            thread = threading.Thread(target=download_file, args=(url, filename))
            threads.append(thread)
            thread.start()  # Start the thread

        # Wait for all threads to finish before proceeding
        for thread in threads:
            thread.join()
        end_time = time.perf_counter()  # End the timer

        # Calculate and print the total download duration
        duration = end_time - start_time
        print(f"Multithreaded download time: {duration:.4f} seconds")

    def test_multithreaded_faster_than_sequential(self):
        """
        Compare the speed of multithreaded download versus sequential download.

        This test ensures that multithreaded downloads are faster than downloading files 
        sequentially. The test times both methods and checks if multithreading is at least 1.5 
        times faster than the sequential method.
        """
        # Sequential download timing
        start_seq = time.perf_counter()  # Start the timer for sequential download
        for url, filename in zip(self.TEST_URLS, self.TEST_FILENAMES):
            # Download each file sequentially
            download_file(url, filename)
        end_seq = time.perf_counter()  # End the timer for sequential download
        sequential_duration = end_seq - start_seq  # Calculate the duration

        # Clean up before the next download test (remove any downloaded files)
        for filename in self.TEST_FILENAMES:
            if os.path.exists(filename):
                os.remove(filename)

        # Multithreaded download timing
        start_thread = time.perf_counter()  # Start the timer for multithreaded download
        threads = []  # List to hold the threads
        for url, filename in zip(self.TEST_URLS, self.TEST_FILENAMES):
            # Create a new thread for each file download
            thread = threading.Thread(target=download_file, args=(url, filename))
            threads.append(thread)
            thread.start()  # Start the thread

        # Wait for all threads to finish before proceeding
        for thread in threads:
            thread.join()
        end_thread = time.perf_counter()  # End the timer for multithreaded download
        multithreaded_duration = end_thread - start_thread  # Calculate the duration

        # Print the durations for comparison
        print(f"Sequential time: {sequential_duration:.4f}s")
        print(f"Multithreaded time: {multithreaded_duration:.4f}s")

        # Assert that multithreading is faster (or at least not worse)
        # It should take less than 1.5 times the time taken by sequential download
        self.assertLess(multithreaded_duration, sequential_duration * 1.5)

if __name__ == '__main__':
    unittest.main()  # Run all tests
