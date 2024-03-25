import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
import re
import struct

myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)  

def dispatcher():
    """
    Main function that runs the loop
    """
    #creat wordlist from text document
    wordlist = textfile_tolist("wordlist.txt")

                                    # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print('Server connected by', address, end=' ')
        print('at', now())
        handleClient(connection, wordlist)

def handleClient(connection, wordlist):
    """
    This function handles client requests
    """

    time.sleep(5)                                # simulate a blocking activity
    while True:                                  # read, write a client socket
        # edited this line just to decode data
        request = connection.recv(1024).decode()
        print(f"Recieved Request: {request}")
        # try except block to catch any issues
        try:
            if not request: break

            # if we get an invalid input respond with a -1 header
            if not is_valid_request(request):
                print("Invalid Input! Replying with error code -1")
                send_response(connection,-1)

            matchlist = return_matches(request,wordlist)

            # if we get no matches, we respond with error -2
            if len(matchlist) == 0:
                print("No matches found! Replying with error code -2")
                send_response(connection,-2)
            
            
            # convert matches to a string and send it as a reply
            matchlist_string = matchlist_to_string(matchlist)
            print("Matches found! Replying with: {matchlist_string}")
            send_response(connection, len(matchlist_string), matchlist_string)

        except Exception as e:
            # if we get an exception, respond with error -3
            print("Exception detected! Replying with error code -3")
            send_response(connection,-3)

    #close connection
    connection.close()

def now():
    return time.ctime(time.time())               # current time on the server

def is_valid_request(request):
    """
    This function checks if there's a valid request
    (ie only letters and wildcards)
    source: https://www.tutorialspoint.com/How-do-I-verify-that-a-string-only-contains-letters-numbers-underscores-and-dashes-in-Python
    """
    # this matches only requests that consist of letters or question marks
    regex_pattern = r'^[a-zA-Z?]+$'
    # test the string against the regex
    if re.match(regex_pattern, request):
        return True  
    else:
        return False 

def does_request_match(request,dict_entry):
    """
    This function returns true if the word in the wordlist (dict_entry) matches the request
    It can also handle wildcards
    """

    # return false if request and entry are different sizes
    if len(request) != len(dict_entry): return False

    # parse through both words, and return false if the letters don't match
    for letter in range(0,len(dict_entry)):
        if not(dict_entry[letter] == request[letter] or request[letter] == '?'):
            return False
        
    return True

def return_matches(request,wordlist):
    """
    this function parses through the wordlist (list from the textfile)
    and returns a list of every item from the wordlist that matches the request
    """
    matchlist = []

    # parse wordlist for items that match
    for word in wordlist:
        if does_request_match(request,word):
            matchlist.append(word)

    return matchlist

def matchlist_to_string(matchlist):
    """
    helper function that converts a matchlist to a string
    code was sourced from here:
    https://www.simplilearn.com/tutorials/python-tutorial/list-to-string-in-python
    """
    return '\n'.join(matchlist)

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

def send_response(connection, code, response=None):
    """
    This function actually sends the response to the client
    for errors, it the response parameter should be omitted and only the code will be sent
    for succeses the response parameter should be filled
    """
    
    # encode and send header int (this is signed)
    response_header_code = struct.pack('!i', code)
    connection.sendall(response_header_code)

    # if the response is filled, then send it as well
    if response:
        encoded_response = response.encode()
        connection.sendall(encoded_response)

# actually run dispatcher
dispatcher()