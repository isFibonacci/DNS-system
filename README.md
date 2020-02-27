# DNS-system

## [How to use]

```
Server :
    Run : 
            ```bash
            $python3 DNSServerV3.py
            ```
    Quit :
            ```bash
            $exit

Client :
    Run :
            ```bash
            $python3 DNSClientV3.py
            ```
    Quit :
            ```bash
            $q
            ```
        
```
## [Description]

1. This program support translate the domain name to the IP addresses.
    For example, Local DNS:google.com: 216.58.216.68
2. For Server :
    - main() :
        Connect to the host by TCP, port : 9989. Spread total 20 threads
    - dnsQuery(connectionSock, srcAddress) :
        1. First check the query is in the local cache or not
        2. If it is, send back to the client, close socket. Save the record in the dns-server-log.csv
        3. If not, call gethostbyname to get the IP and save it at the DNS_mapping.txt
        4. If there is only one IP address, return the IP address
        5. If there are multiple IP addresses, select one and return.

3. For Client :
    - main() :
        Connect to the host by TCP, port : 9989. If input is "q" or "Q", quit the program.
        Otherwise, send the input to server.
        Holding the socket open, the client will wait for the server to respond with a corresponding IPaddress or server cannot find.
        
