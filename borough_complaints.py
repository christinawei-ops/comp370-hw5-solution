#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime

CREATED_DATE_COL = "Created Date"
COMPLAINT_TYPE_COL = "Complaint Type"
BOROUGH_COL = "Borough"



def parse_date(text):
    if not text:
        return None
    for fmt in ("%m/%d/%Y %I:%M:%S %p","%m/%d/%Y %H:%M","%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try:
            return datetime.strptime(text,fmt)
        except ValueError:
            pass

        return None



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", default=None, help="Output CSV file")

    args = parser.parse_args()

    # convert str to time
    start_day = datetime.strptime(args.start, "%Y-%m-%d")
    end_day = datetime.strptime(args.end, "%Y-%m-%d")

    #inclusive to the end of date until 23:59:59
    end_day = end_day.replace(hour=23, minute=59, second=59)

    counts= {}

    with open(args.input, "r", encoding="utf-16") as f:
        #csv reader
        reader = csv.DictReader(f)
        for row in reader:
            #get created date
            created_text = row.get(CREATED_DATE_COL, "")
            created_dt = parse_date(created_text)
            
            complaint = row.get(COMPLAINT_TYPE_COL, "").strip().lower()
            borough = row.get(BOROUGH_COL, "").strip().lower().title()

            #skip lines if needed
            if not complaint or not borough or created_dt is None:
                continue
            if not (start_day <= created_dt <= end_day):
                continue

            key = (complaint, borough)
            counts[key] = counts.get(key, 0) + 1
    
    if args.output:
        out_f = open(args.output, "w")
    else:
        import sys
        out_f = sys.stdout

    writer = csv.writer(out_f)
    writer.writerow(["complaint type", "borough", "count"])

    for (complaint, borough), c in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        writer.writerow([complaint, borough, c])

    if args.output:
        out_f.close()

if __name__ == "__main__":
    main()
