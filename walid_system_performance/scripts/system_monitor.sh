#!/bin/bash
date >> system_logs/system_report.txt
uptime >> system_logs/system_report.txt
free -h >> system_logs/system_report.txt
df -h / >> system_logs/system_report.txt
ps aux --sort=-%cpu | head -4 >> system_logs/system_report.txt
ps aux --sort=-%mem | head -4 >> system_logs/system_report.txt
echo "----------------" >> system_logs/system_report.txt
