# Cloe
Cloe is a CLI tool to store Zoom meeting details and join meetings on the Zoom desktop client.   
It can also remember meeting information to make it convenient to join meetings in the future without having to type in the meeting ID and password every time.  

**Note**: This tool is made for Linux and MacOS. It will not work on Windows.

**Requirements**: Your system should have `python 3.5` or higher to run the `cloe.py` script.  

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
Add a new Zoom meeting that does not require a password:  
`$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id>`  
  
Add a new Zoom meeting that requires a password:  
`$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id> -p <meeting-password>`  

**Note**: Do not include whitespaces in the meeting name when adding a new meeting entry. Use hyphens ('-') or underscores ('\_') instead.  
  

### 2. Join a meeting

#### Quick join a meeting
Quick join a meeting without a password:  
`$ python3 ./cloe.py join <meeting-id>`  

Quick join a meeting with a password:   
`$ python3 ./cloe.py join <meeting-id> <meeting-password>`   

Usage example (joining a meeting **with** a password):   
`$ python3 ./cloe.py join 123456789 012345`   
  
  
#### Join a saved meeting
Before you join a saved meeting, make sure you have saved it's information to Cloe first (refer to _1. Add a new meeting entry_).  
  
Join a saved meeting using the meeting name:  
`$ python3 ./cloe.py join -n <meeting-name>`  
  
Join a saved meeting using the meeting index:  
`$ python3 ./cloe.py join -I <meeting-index>`  
     

### 3. View stored meeting entries
List stored meeting entries:  
`$ python3 ./cloe.py ls`  
  

### 4. Remove a stored meeting entry
Remove a meeting entry:  
`$ python3 ./cloe.py rm -n <meeting-name>`  
  

## Tips
Using an alias makes it a lot more convenient to write out the commands.  

So instead of typing: `python3 path/to/cloe.py join -n my-personal-meeting`  
You can just type in: `cloe join -n my-personal-meeting`  

  
### For Linux: 
Step 1: Open the Terminal and cd to the home directory.  

Step 2: Run `ls -a` and check if there is the `.bashrc` file.    

Step 3: If the `.bashrc` file does not exist, create it by running `touch .bashrc` in the Terminal.   

Step 4: Now run the command `nano .bashrc` to open up the file in the nano editor.  

Step 5: To the last line in the file, add the the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  

Step 6: Press `Ctrl` + `X` and then press `Y` to save the changes you made to the `.bashrc` file. Now close the Terminal.  

Step 7: Open up a fresh Terminal and run the command `source ~/.bashrc` to put into effect the changes you made.  
  
  

### For MacOS:  
Step 1: Open the Terminal and cd to the home directory.  

Step 2: Run `ls -a` and check if there is the `.zshrc` file.    

Step 3: If the `.zshrc` file does not exist, create it by running `touch .zshrc` in the Terminal.     

Step 4: Now run the command `nano .zshrc` to open up the file in the nano editor.  

Step 5: To the last line in the file, add the the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  

Step 6: Press `Cmd` + `X` and then press `Y` to save the changes you made to the `.zshrc` file. Now close the Terminal.  

Step 7: Open up a fresh Terminal and run the command `source ~/.zshrc` to put into effect the changes you made.  


And thats it, now you can use the alias to run Cloe. Run your commands like this:  
`$ cloe join -n my-personal-meeting`  

