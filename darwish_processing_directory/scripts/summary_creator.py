from collections import COunter
from pathlib import Path

monitor_log_name = 'events.log'
monitor_pwd = Path(__file__).resolve().parent.parent.parent / "sarjil_directory_monitoring/logs"
events_log_file = monitor_pwd / monitor_log_name

total_events = []
created_bytes = 0

with open(events_log_file, "r" as f:
	for line in f: # Iterate through the log

		# Check if each line starts an event
		if line.startswith(("MODIFIED", "CREATED", "DELETED")):
			event_type = line.split(':')[0]
			total_events.append(event_type)
			if event_type == 'CREATED':

				# Process the byte size
				try:
					byte_size = next(f)
				except StopIteration:
					pass
				else:
					byte_size = ''.join([c for c in byte_size if c.isdigit()])
					byte_size = int(byte_size)
					
					# Increase byte count for created event
					created_bytes += byte_size

event_counter = Counter(total_events)
print(event_counter)
print(created_bytes)
