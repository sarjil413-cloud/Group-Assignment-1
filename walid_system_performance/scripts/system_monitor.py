#!/usr/bin/env python3
import psutil
import datetime
import os
import time
from pathlib import Path

# Paths
home_dir = Path.home()
log_file = home_dir / "Group-Assignment-1" / "walid_system_performance" / "system_logs" / "system_report.txt"

# Ensure the system_logs folder exists
log_file.parent.mkdir(parents=True, exist_ok=True)

def write_line(text):
    with log_file.open("a") as f:
        f.write(text + "\n")

while True:
	time.sleep(30)
	# 1. Date and Time
	now = datetime.datetime.now()
	load1, load5, load15 = os.getloadavg()

	write_line(now.strftime("%a %b %d %I:%M:%S %p %z"))
	# Format time using strftime
	time_str = now.strftime("%I:%M:%S up %H:%M, 1 user, load average: ")

	# Format load averages
	load_str = "%.2f, %.2f, %.2f" % (load1, load5, load15)

	# Combine them
	line = time_str + load_str
	write_line(line)

	# 2. Memory
	mem = psutil.virtual_memory()
	swap = psutil.swap_memory()
	write_line(f"               total        used        free      shared  buff/cache   available")
	write_line(f"Mem:           {mem.total // (1024**3)}Gi       {mem.used // (1024**3)}Gi       {mem.available // (1024**3)}Gi        0Mi       {mem.buffers // (1024**3)}Gi       {mem.available // (1024**3)}Gi")
	write_line(f"Swap:          {swap.total // (1024**3)}Gi          {swap.used // (1024**3)}B       {swap.free // (1024**3)}Gi")

	# 3. Disk
	disk = psutil.disk_usage('/')
	write_line(f"Filesystem      Size  Used Avail Use% Mounted on")
	write_line(f"/dev/sda2        {disk.total // (1024**3)}G   {disk.used // (1024**3)}G   {disk.free // (1024**3)}G  {disk.percent}% /")

	# 4. Top processes by CPU
	write_line("USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND")
	procs_cpu = sorted(psutil.process_iter(['pid','name','username','cpu_percent','memory_percent','status']), key=lambda p: p.info['cpu_percent'], reverse=True)[:4]
	for p in procs_cpu:
    		write_line(f"{p.info['username']:<12} {p.info['pid']:<5} {p.info['cpu_percent']:<4} {p.info['memory_percent']:<4} 0 0 ?        {p.info['status']:<4} START TIME {p.info['name']}")

	# 5. Top processes by Memory
	write_line("USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND")
	procs_mem = sorted(psutil.process_iter(['pid','name','username','cpu_percent','memory_percent','status']), key=lambda p: p.info['memory_percent'], reverse=True)[:4]
	for p in procs_mem:
    		write_line(f"{p.info['username']:<12} {p.info['pid']:<5} {p.info['cpu_percent']:<4} {p.info['memory_percent']:<4} 0 0 ?        {p.info['status']:<4} START TIME {p.info['name']}")

	write_line("----------------\n")
