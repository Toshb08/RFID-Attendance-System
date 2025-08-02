import time
import boto3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# AWS Configuration
BUCKET_NAME = 'rfid-attendance-logs'
today = time.strftime("%Y-%m-%d")
FILENAME = f"Attendance_{today}.xlsx"
FILE_PATH = os.path.join("C:\\Users\\Toshita\\OneDrive\\Desktop\\RFID", FILENAME)
S3_KEY = FILENAME

# Initialize S3 client using AWS CLI config
s3 = boto3.client('s3')

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Normalize path comparison to avoid slashes/backslashes issues
        if os.path.basename(event.src_path) == FILENAME:
            print("File updated, uploading to S3...")
            try:
                s3.upload_file(FILE_PATH, BUCKET_NAME, S3_KEY)
                print("Upload successful!")
            except Exception as e:
                print(f"Upload failed: {e}")

if __name__ == "__main__":
    path = os.path.dirname(FILE_PATH)
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    print("Watching for file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
