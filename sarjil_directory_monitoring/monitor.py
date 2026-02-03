# Commit 2: Added header comment for clarity
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pwd, grp

# Step 1: Define a handler class to catch events
class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.log_metadata(event.src_path, "CREATED")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"DELETED: {event.src_path} at {time.ctime()}")

    def on_modified(self, event):
        if not event.is_directory:
            self.log_metadata(event.src_path, "MODIFIED")

    def log_metadata(self, filepath, action):
        try:
            stat_info = os.stat(filepath)
            owner = pwd.getpwuid(stat_info.st_uid).pw_name
            group = grp.getgrgid(stat_info.st_gid).gr_name
            print(f"{action}: {filepath}")
            print(f"  Size: {stat_info.st_size} bytes")
            print(f"  Owner: {owner}, Group: {group}")
            print(f"  Permissions: {oct(stat_info.st_mode)[-3:]}")
            print(f"  Last Modified: {time.ctime(stat_info.st_mtime)}")
            print(f"  Created: {time.ctime(stat_info.st_ctime)}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
if __name__ == "__main__":
    path = "monitored_dir"  # folder you want to monitor
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring started on {path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
