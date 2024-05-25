import sys
import csv
import os
import datetime

# subnet dealt with
internal_subnet = '10.10.10.'

# malware ports
c2_ports = ['1337', '1338', '1339', '1340']

# set of ports found to be infected
infected_internal_systems = set()

# set of c2 servers
c2_servers = {}

# check to see if subnet is involved *10.10.10.(...)*
def is_internal(ip):
    return ip.startswith(internal_subnet)

# function to extract the last octet from an IP address, used to sort for the output
def get_last_octet(ip):
    return int(ip.split('.')[-1])

# process connections
def process_connection(connection):
    global infected_internal_systems
    global c2_servers
    
    # parse through data, provided by background document
    connection_time, source_ip, dest_ip, source_port, dest_port, bytes_sent, bytes_received, total_bytes = connection
    
    # check if the source ip is ours, and if it conected with the malicious port(s)
    if is_internal(source_ip) and dest_port in c2_ports:
        infected_internal_systems.add(source_ip)
        if dest_ip in c2_servers:
            c2_servers[dest_ip]['bytes_sent'] += int(bytes_sent)
            if connection_time < c2_servers[dest_ip]['first_connection']:
                c2_servers[dest_ip]['first_connection'] = connection_time
        else:
            c2_servers[dest_ip] = {
                'first_connection': connection_time,
                'bytes_sent': int(bytes_sent)
            }

# take/read csv
def read_csv(filename):
    global infected_internal_systems
    global c2_servers
    
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            process_connection(row)
            
    print("Source File: " + filename)
    print('Systems Infected: {}'.format(len(infected_internal_systems)))
    print('Infected System IPs: {}'.format([f'{ip}' for ip in sorted(infected_internal_systems, key=lambda x: get_last_octet(x))]))
    print('C2 Servers: {}'.format(len(c2_servers)))
    print('C2 Server IPs: {}'.format(sorted(c2_servers.keys())))
    
    utc_time = datetime.timezone(datetime.timedelta(0))
    first_c2_connection = datetime.datetime.fromtimestamp(int(min(c2_servers.values(), key=lambda x: int(x['first_connection']))['first_connection']), utc_time).strftime('%Y-%b-%d %H:%M:%S UTC')
    print('First C2 Connection: {}'.format(first_c2_connection)) 
    print('C2 Data Totals: {}'.format([(ip, c2_servers[ip]['bytes_sent']) for ip in sorted(c2_servers, key=lambda x: c2_servers[x]['bytes_sent'], reverse=True)]))

# error handling
if len(sys.argv) < 2:
    print('Error! - No Log File Specified!')
    sys.exit()

filename = sys.argv[1]

# error handling
if not os.path.isfile(filename):
    print('Error! - File Not Found!')
    sys.exit()
    
read_csv(filename)
