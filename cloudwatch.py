#This python script helps you import logs as CSV based on a search term.
#I wrote it as I was having a hard time scrolling in the console.
import boto3
import csv
from datetime import datetime

# Initialize CloudWatch Logs client
client = boto3.client("logs", region_name="us-east-1")


# Define log group and search term
log_group_name = '#Enter log group here'
search_term = '#Enter search term'  # Corrected search term

# Define start and end times
start_time = int(datetime.strptime('#Define Start_TIme', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
end_time = int(datetime.strptime('#Define End_TIme', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

# Initialize variables for pagination
next_token = None
logs = []

# Fetch logs with pagination
while True:
    if next_token:
        response = client.filter_log_events(
            logGroupName=log_group_name,
            filterPattern=search_term,
            startTime=start_time,
            endTime=end_time,
            nextToken=next_token,
            interleaved=True
        )
    else:
        response = client.filter_log_events(
            logGroupName=log_group_name,
            filterPattern=search_term,
            startTime=start_time,
            endTime=end_time,
            interleaved=True
        )

    logs.extend(response['events'])

    if 'nextToken' not in response:
        break
    next_token = response['nextToken']

# Write logs to a CSV file
with open('#file_name where you want to save', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'message']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for event in logs:
        writer.writerow({
            'timestamp': datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'message': event['message']
        })

print("Logs saved to #file_name where you want to save")
