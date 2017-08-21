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
    u= """Usage: {python|python2|python3} %s [-h | --help] [--mcast-group= | -g ] [--mcast-port= | -p ] [--non-interactive | -n] [--data-only | -d] [--max-packets= | -m ] [--send-interval= | -s ]
    -h|--help            : This help screen
    -g|--mcast-group     : Multicast group to listen on
    -p|--mcast-port      : Multicast port to listen on
    -n|--non-interactive : Run in non-interactive mode (do not wait for ENTER key before listening)
    -d|--data-only       : Do not display information before listening. This changes output as well to make it more parseable by scripts.
                           It also automatically enables -n.
    -m|--max-packets     : max number of packets to send before quitting. Default: never quit.
    -s|--send-interval   : how much to sleep in milliseconds, between sending the packets. 0: flood the interface. Default: 150
                           It is not recommended to flood the buffers. You will get a very small throughput
                           It is better to set -s 0.01 (yes, fractions are allowed). Max I managed to get before flooding occured was:
                           -s 0.004 if just sending, or -s 0.0015 if sending and receiving on same interface. This MAY overload the interface.
""" %n
    sys.stdout.write("%s\n" %u)

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

try:
    opts, args = getopt.getopt(sys.argv[1:], "hg:p:ndm:s:", ["help", "mcast-group=","mcast-port=","non-interactive","data-only","max-packets=","send-interval="])
except getopt.GetoptError as err:
    sys.stdout.write("%s\n" %str(err))
    sys.stdout.flush()
    usage()
    sys.exit(2)
interactive=True
info=True
maxCount=0
sendInterval=150.0
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
    elif o in ("-m","--max-packets"):
        maxCount = int(a)
    elif o in ("-s","--send-interval"):
        sendInterval = float(a)
    else:
        usage()

def printer(q):
    global packCount
    global maxCount
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
            sys.stdout.write("60-sec Avg Packets/second sent: %s\t\tPackets in Last Second sent: %s\t\tTotal packets sent:%s\n" %(avgPerSec,lastSecond,packCount))
        else:
            sys.stdout.write("avg_packets_per_second_sent=%s packets_sent_in_last_second=%s total_packets_sent=%s\n" %(avgPerSec,lastSecond,packCount))
        sys.stdout.flush()

if info == True:
    if interactive==True:
        sys.stdout.write("PRESS ENTER TO START SENDING ON: %s:%s" %(MCAST_GRP,MCAST_PORT))
    else:
        sys.stdout.write("SENDING ON: %s:%s" %(MCAST_GRP,MCAST_PORT))
    sys.stdout.flush()
    if interactive==True:
        raw_input()
    sys.stdout.write("\n\n")
    sys.stdout.flush()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
packCount=0
q = Queue()
t = threading.Thread(target=printer, args=(q,))
t.start()

while (maxCount==0)or(packCount<maxCount):
    try:
        try:
            sock.sendto("robot", (MCAST_GRP, MCAST_PORT))
            time.sleep(sendInterval/1000.0)
            packCount=packCount+1
        except socket.error as e:
            if "No buffer space available" in str(e):
                sys.stdout.write("THROTTLING BACK 1 SECOND, INTERFACE FLOODED: %s\n" %str(e))
                sys.stdout.flush()
                time.sleep(1)
                pass
            else:
                raise
    except KeyboardInterrupt:
        q.put("QuitNow")
        raise
    except Exception:
        q.put("ExceptNow")
        raise
q.put("Finito")

