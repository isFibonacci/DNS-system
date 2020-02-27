# Spring 2020 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os, random
from socket import *

def main():
	host = "localhost" # Hostname. It can be changed to anything you desire.
	port = 9982 # Port number.

	#create a socket object, SOCK_STREAM for TCP
	try :
		serverSocket = socket(AF_INET, SOCK_STREAM)
	except :
		serverSocket = None # Handle exception

	#bind socket to the current address on port 5001
	try :
		serverSocket.bind((host, port))
		
		#Listen on the given socket maximum number of connections queued is 20
		serverSocket.listen(20)
	except:
		serverSocket = None # Handle exception

	if not serverSocket :
		print("Error: cannot open socket")
		sys.exit(1) # If the socket cannot be opened, quit the program.

	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()

	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port 9989
		connectionSock, addr = serverSocket.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

def dnsQuery(connectionSock, srcAddress):
	
	serverSocket = connectionSock
	
	# accept query
	query = serverSocket.recv(1024).decode().strip('\n')
	found = False

	#check the DNS_mapping.txt to see if the host name exists
	#set local file cache to predetermined file.
	try :
		cache = open("DNS_mapping.txt", 'r')
		cache.close()
	except:
		#create file if it doesn't exist 
		cache = open('DNS_mapping.txt', 'w')
		cache.close()

	try :
		log = open("dns-server-log.csv", 'a')
	except:
		#create file if it doesn't exist 
		cache = open('dns-server-log.csv', 'w')

	#if it does exist, read the file line by line to look for a
	#match with the query sent from the client
	#If match, use the entry in cache.

	with open('DNS_mapping.txt', 'r') as cache:
		for record in cache:
			recordHost = str((record).split(',')[0])

			if recordHost == query :
				found = True 
				ip = (str((record).split(', ')[1])).strip('\n')
				log.write(query + ', ' + ip+'\n')

				#print response to the terminal
				print(query + ', ' + ip+'\n')

				serverSocket.send(('Local DNS: '+query+' : '+ip).encode())
				serverSocket.close()
	
	cache.close()
	log.close()

	
	#However, we may get multiple IP addresses in cache, so call dnsSelection to select one.
	#If no lines match, query the local machine DNS lookup to get the IP resolution
	if not found:
		#If no lines match, query the local machine DNS lookup to get the IP resolution
		cache = open('DNS_mapping.txt', 'a')
		log = open('dns-server-log.csv', 'a')
		try :
			response = gethostbyname(query)
			
			#write the response in DNS_mapping.txt
			cache.write(query+', '+response+'\n')
			cache.close()
			log.write(query + ', ' + response+'\n')
			log.close()
			ans = 'API DNS: '+query + ' : ' + response+'\n'

			#print response to the terminal
			print(query + ', '+response)

			#send the response back to the client
			serverSocket.send(ans.encode())
			
			#Close the server socket.
			serverSocket.close()
		except :
			response = 'server cannot find '

			#write the response in DNS_mapping.txt
			cache.write(query+', '+response+query+'\n')
			cache.close()
			log.write(query+', '+response+query+'\n')
			log.close()
			ans = query + ', ' + response+'\n'

			#print response to the terminal
			print(ans)

			#send the response back to the client
			serverSocket.send(ans.encode())
			
			#Close the server socket.
			serverSocket.close()
	
  
# def dnsSelection(ipList):
	#checking the number of IP addresses in the cache
	#if there is only one IP address, return the IP address
	#if there are multiple IP addresses, select one and return.
	##bonus project: return the IP address according to the Ping value for better performance (lower latency)
	# pass


def monitorQuit():
	while 1:
		sentence = input()
		if sentence == "exit":
			os.kill(os.getpid(),9)

main()
