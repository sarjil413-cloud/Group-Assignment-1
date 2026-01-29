#!/bin/bash
date >> ~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
uptime >>~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
free -h >> ~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
df -h / >> ~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
ps aux --sort=-%cpu | head -4 >>~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
ps aux --sort=-%mem | head -4 >> ~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
echo "----------------" >> ~/Group-Assignment-1/walid_system_performance/system_logs/system_report.txt
# This command collects memory usage
# This command logs disk usage
