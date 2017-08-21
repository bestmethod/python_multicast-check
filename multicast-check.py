import socket
import struct
import sys
import threading
import time
try:
    from Queue import Queue
except:
    from queue import Queue
import getopt

def usage():
    n=sys.argv[0]
    u= """Usage: {python|python2|python3} %s [-h | --help] [--mcast-group | -g] [--mcast-port | -p] [--non-interactive | -n] [--data-only | -d]
    -h|--help            : This help screen
    -g|--mcast-group     : Multicast group to listen on
    -p|--mcast-port      : Multicast port to listen on
    -n|--non-interactive : Run in non-interactive mode (do not wait for ENTER key before listening)
    -d|--data-only       : Do not display information before listening. This changes output as well to make it more parseable by scripts.
                           It also automatically enables -n.
""" %n
    sys.stdout.write("%s\n" %u)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

try:
    opts, args = getopt.getopt(sys.argv[1:], "hg:p:nd", ["help", "mcast-group=","mcast-port=","non-interactive","data-only"])
except getopt.GetoptError as err:
    sys.stdout.write("%s\n" %str(err))
    sys.stdout.flush()
    usage()
    sys.exit(2)
interactive=True
info=True
for o, a in opts:
    if o in ("--non-interactive","-n"):
        interactive=False
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-g", "--mcast-group"):
        MCAST_GRP=a
    elif o in ("-p", "--mcast-port"):
        MCAST_PORT=int(a)
    elif o in ("-d","--data-only"):
        info=False
    else:
        usage()

def printer(q):
    global packCount
    global info
    prevPackCount=0
    lastMinute=[]
    while q.empty():
        time.sleep(1)

        lastSecond=packCount-prevPackCount

        if len(lastMinute) == 10:
            lastMinute = lastMinute[1:]
        lastMinute.append(lastSecond)

        prevPackCount=packCount

        avgPerSec=int(sum(lastMinute)/len(lastMinute))
        if info == True:
            sys.stdout.write("60-sec Avg Packets/second: %s\t\tPackets in Last Second: %s\t\tTotal packets:%s\n" %(avgPerSec,lastSecond,packCount))
        else:
            sys.stdout.write("avg_packets_per_second=%s packets_received_in_last_second=%s total_packets_received=%s\n" %(avgPerSec,lastSecond,packCount))
        sys.stdout.flush()

if info == True:
    sys.stdout.write("\nFor aerospike multicast, packet averages should be per formula: number_of_nodes * (1000 / heartbeat-interval)\n\nIf you are seeing less than that, then mcast is having issues.\n\nIf you see only (1000 / heartbeat-interval), then the node can only see own mcast, i.e. mcast totally broken.\n\nIf you can see 0 mcast at all, check you are listening on correct group and port as per aerospike config. If so, the node's net interface does not support mcast.\n\n")
if info == True:
    if interactive==True:
        sys.stdout.write("PRESS ENTER TO START LISTENING ON: %s:%s" %(MCAST_GRP,MCAST_PORT))
    else:
        sys.stdout.write("LISTENING ON: %s:%s" %(MCAST_GRP,MCAST_PORT))
    sys.stdout.flush()
    if interactive==True:
        raw_input()
    sys.stdout.write("\n\n")
    sys.stdout.flush()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
packCount=0
q = Queue()
t = threading.Thread(target=printer, args=(q,))
t.start()

while True:
    try:
        sock.recv(10240)
        packCount=packCount+1
    except KeyboardInterrupt:
        q.put("QuitNow")
        raise
