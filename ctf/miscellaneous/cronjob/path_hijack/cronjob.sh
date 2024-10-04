#!/bin/bash

export PATH=/app/uploads:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Ensure the uploaded 'ls' file is executable
if [ -f "/app/uploads/ls" ]; then
    chmod +x /app/uploads/ls
fi

# Log the execution time and environment to a file
echo "Cron job executed at $(date)" >> /app/cronlog.txt
echo "PATH: $PATH" >> /app/cronlog.txt
echo "Contents of uploads directory:" >> /app/cronlog.txt
ls -l /app/uploads >> /app/cronlog.txt 2>&1

# Simulate a command that uses system binaries (ls in this case)
ls > /dev/null 2>&1

# Check if flag exists in the uploads directory
if [ -f "/app/uploads/flag.txt" ]; then
    echo "Flag file copied successfully." >> /app/cronlog.txt
else
    echo "Flag file not found after job." >> /app/cronlog.txt
fi
