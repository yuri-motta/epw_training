import subprocess, re

list_of_ips = ["facebook.com", "google.com"]
for ip in list_of_ips:
    ping_process = subprocess.Popen(['ping', '-c', '1', ip], stdout=subprocess.PIPE)
    stdout = ping_process.stdout.read()
    match = re.search(r'\d*\.\d*\/(\d*\.\d*)\/\d*\.\d*\/\d*\.\d*', stdout)
    avg = match.group(1)
    print('{}: {}ms'.format(ip, avg))