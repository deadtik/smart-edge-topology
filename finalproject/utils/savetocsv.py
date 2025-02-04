# utils/savetocsv.py

import csv

def save_data_to_csv(filename, data):
    print(f"Saving data to {filename}: {data}")  # Debug print statement
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['topology', 'latency', 'throughput', 'packet_loss', 'bandwidth', 'jitter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is empty (for the first run)
        csvfile.seek(0, 2)
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the data
        writer.writerow(data)