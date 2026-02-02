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
system_report_file = system_log_pwd / system_log_name

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

# GET THE SYSTEM REPORT

records = 0
load_averages = []
mem_total = []
mem_used = []
disk_size = 0
disk_perc_use = []

with open(system_report_file, "r") as f:
	for line in f:
		if line == '-'*16: # This shows a new record
			records += 1
		
		# LOAD AVERAGE
		if 'load average' in line:
			pcstat = line.split(':')
			current_load_averages = pcstat[4].strip().replace(" ","").split(",")
			load_avg_1min = float(current_load_averages[0])
			load_averages.append(load_avg_1min)

		# MEMORY
		if line.startswith('Mem:'):
			current_mem = line.split() # Splits the mem line into multiple parts
			current_total = float(current_mem[1].replace("Gi", ""))
			current_used = float(current_mem[2].replace("Gi", ""))
			mem_total.append(current_total)
			mem_used.append(current_used)
		
		# DISK
		if line.startswith(r"/dev/"):
			disk_stats = line.split()
			disk_size = int(disk_stats[1].replace("G",""))
			disk_percentage = int(disk_stats[4].replace("%", ""))
			disk_perc_use.append(disk_percentage)

# SYSTEM REPORT STATS

average_load = sum(load_averages)/len(load_averages)
average_mem_used = sum((used/total)*100 for used, total in zip(mem_used, mem_total))
average_disk_used = sum(disk_perc_use)/len(disk_perc_use)

# CREATE THE SUMMARY

current_date = date.today()
current_timelog = datetime.now()
summary_file_name = "summary_" + str(current_date) + ".txt"
with open(summary_pwd / summary_file_name, "w") as f:
	
	# DIRECTORY MONITORING
	log = str(current_timelog) + "\n" + "=" * 25 # Get the current time
	log += f"\n\nDirectory Monitoring:\n\nFiles created: {event_counter['CREATED']} ({created_bytes} bytes created)"
	log += f"\nFiles modified: {event_counter['MODIFIED']}"
	log += f"\nFiles deleted: {event_counter['DELETED']}"

	# SYSTEM REPORTING
	log += f"\n\nSystem Reports:\nSnapshots: {records}"
	log += f"\n\nAvg. Load(1 min): {average_load}\nLast Avg. Load(1 min): {load_averages[-1]}"

	f.write(log)

print("Summary successfully created")
