## Message Configuration

# Message Headers

- Requests are just the string of the word

- Responses are an integer, followed by the string of words generated. each word in the response is seperated by a newline character

- Successes from the server are indicated by a positive integer indicating that there has been a word found
- Faiures are indicated by a negative number:
    - -1 = Invalid Request (non numerical (or wildcard) characters/corrupted request )
    - -2 = No items found 
    - -3 = Error on the server's end
    -