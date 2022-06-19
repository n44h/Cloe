# Cloe
Cloe is a tool to store Zoom meeting details and join meetings on the Zoom desktop client using the CLI.  

**Note**: This tool is made for Linux and MacOS. It will not work on Windows.

## Keyword Arguments

#### Cloe takes 4 arguments:  

`--mname`  - meeting name (short)  

`--mindex` - meeting index (the index position of the meeting in the zoom_meetings.json file)  

`--mid`    - meeting ID  

`--mpw`    - meeting password (optional)  
 
#### Flags for keyword arguments 

`--mname`  -> `-n`  

`--mindex` -> `-I`  

`--mid`    -> `-i`  

`--mpw`    -> `-p`  

## Commands
#### Cloe performs 4 actions:

`ls`, `join`, `add`, and `rm`  
  
### 1. Add a new meeting entry for Cloe to remember
Add a new meeting entry that doesn't need a password:  
`$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id>`  
  
Add a new meeting entry with a password:  
`$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id> -p <meeting-password>`  
  

### 2. Join a meeting
Before you join a meeting, make sure you have added the Zoom meetings information to Cloe first (refer to _1. Add a new meeting entry_).  
  
Join a meeting using the meeting name:  
`$ python3 ./cloe.py join -n <meeting-name>`  
  
Join a meeting using the meeting index:  
`$ python3 ./cloe.py join -I <meeting-index>`  
     

### 3. View stored meeting entries
List stored meeting entries:  
`$ python3 ./cloe.py ls`  
  

### 4. Remove a stored meeting entry from Cloe
Remove a meeting entry:  
`$ python3 ./cloe.py rm -n <meeting-name>`  
  
