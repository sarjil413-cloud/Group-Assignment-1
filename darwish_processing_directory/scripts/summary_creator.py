from datetime import date, datetime
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

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

# GET THE SYSTEM REPORT

records = 0
load_averages = []
mem_total = []
mem_used = []
disk_size = 0
disk_perc_use = []

with open(system_report_file, "r") as f:
	for line in f:
		if line.startswith("--------"): # This shows a new record
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
	#-- AVERAGE LOAD REPORT
	log += f"\n\nSystem Reports:\nSnapshots: {records}"
	log += f"\n\nAvg. Load(1 min): {average_load:.2f}\nCurrent Avg. Load(1 min): {load_averages[-1]}"
	#-- MEMORY REPORT
	log += f"\n\nTotal Memory: {mem_total[-1]}Gi\nCurrent Memory Used: {mem_used[-1]}Gi\nAverage Memory Usage: {average_mem_used:.2f}%"
	#-- DISK REPORT
	log += f"\n\nDisk Size: {disk_size}\nCurrent Disk Used (Percentage): {disk_perc_use[-1]}%\nAverage Disk Used (Percentage): {average_disk_used}%"

	f.write(log)


print("Summary successfully created") # PING USER THAT SUMMARY IS DONE!

################# VISUAL SUMMARY TIME

# CREATING BAR CHART

bar_categories = np.array(["Created", "Modified", "Deleted"])
bar_values = np.array([event_counter['CREATED'], event_counter['MODIFIED'], event_counter['DELETED']])
colors = ["green", "blue", "red"]

plt.bar(bar_categories, bar_values, color=colors)
plt.xlabel("Events")
plt.ylabel("Occurrances")
plt.title("RECORD OF EVENTS (DIR. MONITORING)")

plt.savefig(summary_pwd / "events_barchart.png")

# CREATING PIE CHART OF MEMORY USAGE AND DISK USAGE

def CreatePieChart(ax, val, category, title):
	ax.pie(val, labels=category, autopct="%1.1f%%", startangle=90)
	ax.set_title(title)
	ax.axis('equal')
	return ax

pie_cat_1 = np.array(["Available Memory", "Memory Used"])
pie_val_1 = np.array([mem_total[-1] - mem_used[-1], mem_total[-1]])

disk_usage = disk_size*(average_disk_used/100)
pie_cat_2 = np.array(["Available disk", "Disk Used"])
pie_val_2 = np.array([disk_size - disk_usage, disk_usage])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

#-- MEMORY
ax1 = CreatePieChart(ax1, pie_val_1, pie_cat_1, 'MEMORY DISTRIBUTION')

#-- DISK
ax2 = CreatePieChart(ax2, pie_val_2, pie_cat_2, 'DISK DISTRIBUTION')

# SAVE PIE CHART
plt.tight_layout()
plt.savefig(summary_pwd / "system_distribution.png")
