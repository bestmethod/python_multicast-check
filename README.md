# python_multicast-check
Multicast check for send-receive in order to test if multicast works and how many packets are being exchanged.
### Disclaimer: I hold no responsibility if you break anything, cause or get any loss or destroy the planet while running this (even though it should be safe). You have the potential to flood network interfaces with multicast packets, which may take the whole network down, so use with caution and some thought. You have been warned. Defaults (150msec sleep interval) are very safe, so you are ok.

Receive:
```
$ python multicast-check.py -h
Usage: {python|python2|python3} multicast-check.py [-h | --help] [--mcast-group | -g] [--mcast-port | -p] [--non-interactive | -n] [--data-only | -d]
    -h|--help            : This help screen
    -g|--mcast-group     : Multicast group to listen on
    -p|--mcast-port      : Multicast port to listen on
    -n|--non-interactive : Run in non-interactive mode (do not wait for ENTER key before listening)
    -d|--data-only       : Do not display information before listening. This changes output as well to make it more parseable by scripts.
                           It also automatically enables -n.
```

Send:
```
$ python multicast-send.py -h
Usage: {python|python2|python3} multicast-send.py [-h | --help] [--mcast-group= | -g ] [--mcast-port= | -p ] [--non-interactive | -n] [--data-only | -d] [--max-packets= | -m ] [--send-interval= | -s ]
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
```

Example receive:
```
$ python multicast-check.py -d
avg_packets_per_second=1083 packets_received_in_last_second=10836 total_packets_received=10836
avg_packets_per_second=6383 packets_received_in_last_second=52996 total_packets_received=63832
avg_packets_per_second=11772 packets_received_in_last_second=53892 total_packets_received=117724
avg_packets_per_second=17115 packets_received_in_last_second=53430 total_packets_received=171154
avg_packets_per_second=22503 packets_received_in_last_second=53883 total_packets_received=225037
avg_packets_per_second=27896 packets_received_in_last_second=53924 total_packets_received=278961
avg_packets_per_second=29127 packets_received_in_last_second=12309 total_packets_received=291270
avg_packets_per_second=33245 packets_received_in_last_second=41185 total_packets_received=332455
avg_packets_per_second=38593 packets_received_in_last_second=53482 total_packets_received=385937
avg_packets_per_second=43965 packets_received_in_last_second=53721 total_packets_received=439658
avg_packets_per_second=48231 packets_received_in_last_second=53488 total_packets_received=493146
avg_packets_per_second=48131 packets_received_in_last_second=51997 total_packets_received=545143
avg_packets_per_second=48113 packets_received_in_last_second=53713 total_packets_received=598856
avg_packets_per_second=48161 packets_received_in_last_second=53910 total_packets_received=652766
avg_packets_per_second=48143 packets_received_in_last_second=53705 total_packets_received=706471
avg_packets_per_second=48133 packets_received_in_last_second=53821 total_packets_received=760292
```

Example send:
```
$ python multicast-send.py -s 0.001 -d
avg_packets_per_second_sent=52739 packets_sent_in_last_second=52739 total_packets_sent=52739
avg_packets_per_second_sent=53306 packets_sent_in_last_second=53874 total_packets_sent=106613
avg_packets_per_second_sent=53454 packets_sent_in_last_second=53751 total_packets_sent=160364
avg_packets_per_second_sent=53608 packets_sent_in_last_second=54068 total_packets_sent=214432
avg_packets_per_second_sent=53651 packets_sent_in_last_second=53825 total_packets_sent=268257
THROTTLING BACK 1 SECOND, INTERFACE FLOODED: [Errno 55] No buffer space available
avg_packets_per_second_sent=48544 packets_sent_in_last_second=23012 total_packets_sent=291269
avg_packets_per_second_sent=45972 packets_sent_in_last_second=30540 total_packets_sent=321809
avg_packets_per_second_sent=46906 packets_sent_in_last_second=53439 total_packets_sent=375248
avg_packets_per_second_sent=47638 packets_sent_in_last_second=53496 total_packets_sent=428744
avg_packets_per_second_sent=48277 packets_sent_in_last_second=54028 total_packets_sent=482772
avg_packets_per_second_sent=48344 packets_sent_in_last_second=53416 total_packets_sent=536188
avg_packets_per_second_sent=48153 packets_sent_in_last_second=51963 total_packets_sent=588151
avg_packets_per_second_sent=48169 packets_sent_in_last_second=53908 total_packets_sent=642059
avg_packets_per_second_sent=48143 packets_sent_in_last_second=53808 total_packets_sent=695867
avg_packets_per_second_sent=48122 packets_sent_in_last_second=53618 total_packets_sent=749485
avg_packets_per_second_sent=51194 packets_sent_in_last_second=53731 total_packets_sent=803216
avg_packets_per_second_sent=53504 packets_sent_in_last_second=53641 total_packets_sent=856857
avg_packets_per_second_sent=53490 packets_sent_in_last_second=53299 total_packets_sent=910156
avg_packets_per_second_sent=53546 packets_sent_in_last_second=54051 total_packets_sent=964207
avg_packets_per_second_sent=53517 packets_sent_in_last_second=53742 total_packets_sent=1017949
avg_packets_per_second_sent=53545 packets_sent_in_last_second=53689 total_packets_sent=1071638
```
