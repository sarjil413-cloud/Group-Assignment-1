from datetime import date, datetime
from collections import Counter
from pathlib import Path

# FILE
current_pwd = Path(__file__).resolve()
parent_folder = current_pwd.parent.parent
repos = parent_folder.parent

# SUMMARY FILE PATHS
summary_pwd = parent_folder / "summaries"

# EVENT FILE PATHS
monitor_log_name = 'events.log'
monitor_pwd = repos / "sarjil_directory_monitoring/logs"
events_log_file = monitor_pwd / monitor_log_name

total_events = []
created_bytes = 0

# SYSTEM REPORTS

system_log_name = 'system_report.txt'
system_log_pwd = repos / "walid_system_performance/system_logs"
system_report_file = system_log_pwd / system_load_name

# GET EVENTS

with open(events_log_file, "r") as f:
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

# CREATE THE SUMMARY

current_date = date.today()
current_timelog = datetime.now()
summary_file_name = "summary_" + str(current_date) + ".txt"
with open(summary_pwd / summary_file_name, "w") as f:
	
	log = str(current_timelog) + "\n" + "=" * 25 # Get the current time
	log += f"\n\nDirectory Monitoring:\n\nFiles created: {event_counter['CREATED']} ({created_bytes} bytes created)"
	log += f"\nFiles modified: {event_counter['MODIFIED']}"
	log += f"\nFiles deleted: {event_counter['DELETED']}"

	f.write(log)

print("Summary successfully created")
