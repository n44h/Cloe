# Cloe User Guide

User guide covers the commands in Cloe v2.0.0+.  

This guide assumes that you have set up an alias for Cloe. If you have not set up an 
alias for Cloe, just replace `cloe` with `python3 path/to/cloe.py` in the following 
commands.  

### Requirements
* Python 3.5+
* Zoom Desktop Client installed on your system
* Additionally, staying logged in on the Zoom Desktop Client will help avoid 
  any unexpected errors  
&nbsp;  
___

## Commands  

#### Cloe performs 5 actions:

`add`, `join`, `ls`, `rm`, `clear`  

### 1. Save a new meeting for Cloe to remember  

* Save a new Zoom meeting that does not require a password:  
    ```commandline
    $ cloe add <meeting-name> <meeting-id>  
    ```  

* Save a new Zoom meeting that requires a password:  
    ```commandline
    $ cloe add <meeting-name> <meeting-id> <meeting-password>  
    ```

**Note**: Meeting names should not contain whitespaces.  
___   

### 2. Join a meeting

#### Quick join a meeting
* Quick join a meeting without a password:  
    ```commandline
    $ cloe join -q <meeting-id>  
    ```  

* Quick join a meeting with a password:   
    ```commandline
    $ cloe join -q <meeting-id> <meeting-password>  
    ```
  

#### Join a saved meeting
* Join a saved meeting using the meeting name:  
    ```commandline
    $ cloe join <meeting-name>  
    ```  

* Join a saved meeting using the meeting index:  
    ```
    $ cloe join <meeting-index>  
    ```  
&nbsp;

##### Usage:
```commandline
$ cloe join -q 123-4567-8901 
```  
```commandline
$ cloe join my-meeting 
```  
```commandline
$ cloe join 4 
```  

**Note**: The meeting index can be found by listing the saved meeting.
___  

### 3. List saved meetings  

* List the **names** and **IDs** of all the saved meetings:  
    ```commandline
    $ cloe ls
    ```
  
* List only the **names** all the saved meetings:  
    ```commandline
    $ cloe ls -n
    ```  
  
* List the **names**, **IDs**, and **passwords** of all the saved meetings:  
    ```commandline
    $ cloe ls -p
    ```
___

### 4. Remove a saved meeting
```commandline
$ cloe rm <meeting-name>  
```  

Meetings can only be removed by name.  
___

### 5. Clear all saved meetings  
This removes all saved meetings from Cloe. 
```commandline
$ cloe clear
```  

Cloe will prompt the user for confirmation before clearing the saved meetings.  
___