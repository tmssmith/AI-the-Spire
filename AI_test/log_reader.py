import sys
import argparse
import os
import json

def main(log):
    filename = os.path.basename(log)
    f = open(filename, "r")
    log_str = f.read()
    log_str = log_str.replace('DEBUG:root:Read:', '')
    log_str = log_str.splitlines()
    del log_str[0]

    log_data = json.loads(log_str[2])
    print(log_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log", help = "Filepath and name for gameplay logs")
    args = parser.parse_args()
    log = args.log
    main(log)
