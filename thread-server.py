"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow up to 5 pending connects

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    time.sleep(5)                                # simulate a blocking activity
    while True:                                  # read, write a client socket
        data = connection.recv(1024)
        if not data: break
        reply = 'Echo=>%s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()

def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print('Server connected by', address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient, (connection,))

# dispatcher()

def does_request_match(request,dict_entry):
    if len(request) != len(dict_entry): return False

    for letter in range(0,len(dict_entry)):
        if not(dict_entry[letter] == request[letter] or request[letter] == '?'):
            return False
        
    return True

def return_matches(request,dict_dir):
    wordlist = textfile_tolist(dict_dir)

    matchlist = []

    for word in wordlist:
        if does_request_match(request,word):
            matchlist.append(word)

    return matchlist

def textfile_tolist(dict_dir):
    """
    simple function that converts a text file into a large list
    the code in here was sourced from:
    https://www.geeksforgeeks.org/how-to-read-text-file-into-list-in-python/
    """
    # open file
    my_file = open(dict_dir, "r") 
  
    # reading the file 
    data = my_file.read() 
    
    # replacing end splitting the text  
    # when newline ('\n') is seen. 
    data_into_list = data.split("\n") 
    my_file.close() 

    # return list
    return data_into_list

match = return_matches("a?e","wordlist.txt")
print(len(match))
print(match)
