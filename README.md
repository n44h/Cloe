# Cloe
Cloe is a CLI tool to join Zoom meetings on the Zoom desktop client. Cloe also makes it convenient to join recurring meetings using just a unique meeting name, so that you don't have to type in the meeting ID and password every time.     

This tool works on Linux, macOS, and Windows.  

**Requirements**: _Python 3.5_ or higher is required to run the `cloe.py` script.  

**Security Warning**: Note that the saved meeting IDs and meeting passwords are stored in a JSON file. If this is considered too risky by you, **do not** save your meeting details in Cloe.   

___

## Arguments

#### Cloe can take 4 arguments:  

1. `--mname`  - meeting name   

2. `--mindex` - meeting index   

3. `--mid`    - meeting ID  

4. `--mpw`    - meeting password (optional)  

**Note**: The meeting index can be found by listing the saved meeting entries; refer to _3. View saved meeting entries_.   

#### Short Arguments 

Long option | Short option  
---- | ----
`--mname` | `-n`  
`--mindex` | `-I`  
`--mid` | `-i`  
`--mpw` | `-p`  

___

## Commands  

#### Cloe performs 4 actions:

`add`, `join`, `ls`, and `rm`  

### 1. Save a new meeting for Cloe to remember  

* Save a new Zoom meeting that does not require a password:  
```
$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id>  
```  

* Save a new Zoom meeting that requires a password:  
```
$ python3 ./cloe.py add -n <meeting-name> -i <meeting-id> -p <meeting-password>  
```  

**Note**: Do not include whitespaces in the meeting name when adding a new meeting entry. Use hyphens ('-') or underscores ('\_') instead.  

___   

### 2. Join a meeting

#### Quick join a meeting
* Quick join a meeting without a password:  
```
$ python3 ./cloe.py join <meeting-id>  
```  

* Quick join a meeting with a password:   
```
$ python3 ./cloe.py join <meeting-id> <meeting-password>  
```   

Usage example (joining a meeting **with** a password):   
```
$ python3 ./cloe.py join 123456789 012345   
```  

#### Join a saved meeting
Before you join a saved meeting, make sure you have saved it's information to Cloe first (refer to _1. Add a new meeting entry_).  

* Join a saved meeting using the meeting name:  
```
$ python3 ./cloe.py join -n <meeting-name>  
```  

* Join a saved meeting using the meeting index:  
```
$ python3 ./cloe.py join -I <meeting-index>  
```  

**Note**: The meeting index can be found by listing the saved meeting entries; refer to _3. View saved meeting entries_. 

___  

### 3. View saved meeting entries  

List all the saved meeting entries:  
```
$ python3 ./cloe.py ls  
```  

___

### 4. Remove a saved meeting entry  

Remove a meeting entry:  
```
$ python3 ./cloe.py rm -n <meeting-name>  
```  

___

## Tips
Using an alias makes it a lot more convenient to write out the commands.  

For instance, instead of typing:  
```
$ python3 path/to/cloe.py join -n my-personal-meeting   
```  
You can just type in:  
```
$ cloe join -n my-personal-meeting  
```  

### For Linux: 
* **Step 1:** Open the Terminal and cd to the home directory.  

* **Step 2:** Run `ls -a` and check if there is a `.bashrc` file.    

* **Step 3:** If the `.bashrc` file does not exist, create it by running `touch .bashrc` in the Terminal.   

* **Step 4:** Now run the command `nano .bashrc` to open up the file in the nano editor.  

* **Step 5:** To the last line in the file, add the the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  

* **Step 6:** Press `Ctrl` + `X` and then press `Y` to save the changes you made to the `.bashrc` file. Now close the Terminal.  

* **Step 7:** Open up a fresh Terminal and run the command `source ~/.bashrc` to put into effect the changes you made.  

___

### For MacOS:  
* **Step 1:** Open the Terminal and cd to the home directory.  

* **Step 2:** Run `ls -a` and check if there is the `.zshrc` file.    

* **Step 3:** If the `.zshrc` file does not exist, create it by running `touch .zshrc` in the Terminal.     

* **Step 4:** Now run the command `nano .zshrc` to open up the file in the nano editor.  

* **Step 5:** To the last line in the file, add the the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  

* **Step 6:** Press `Cmd` + `X` and then press `Y` to save the changes you made to the `.zshrc` file. Now close the Terminal.  

* **Step 7:** Open up a fresh Terminal and run the command `source ~/.zshrc` to put into effect the changes you made.  


And thats it, you've set up a clean short alias to run Cloe.  

From now on, you can run your commands for Cloe like this:  
```
$ cloe join -n <meeting-name>
```

