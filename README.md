# Cloe
Cloe is a CLI tool to join Zoom meetings with the Zoom Desktop Client. Cloe also makes it convenient 
to join recurring meetings using a unique meeting name, so that you don't have to type in the meeting ID and 
password every time.     

This tool works on Linux, macOS, and Windows.  

**Requirements**: _Python 3.5_ or higher is required to run `cloe.py`.   

Refer to the [User Guide](USER_GUIDE.md) for instructions on how to use Cloe.
___

## Setup Alias
Using an alias makes it a lot more convenient to write out the commands.  

For instance, instead of typing:  
```commandline
$ python3 path/to/cloe.py join my-meeting   
```  
You can just type in:  
```commandline
$ cloe join my-meeting  
```  

### Creating an Alias in Linux: 
1. Open the Terminal and cd to the home directory.  
&nbsp;  
2. Enter `ls -a` and check if there is a `.bashrc` file.    
&nbsp;  
3. If the `.bashrc` file does not exist, create it by running `touch .bashrc` in the Terminal.   
&nbsp;  
4. Now run the command `nano .bashrc` to open up the file in the nano editor.  
&nbsp;  
5. On a fresh line at the end of the file, add the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  
&nbsp;  
6. Press <kbd>Ctrl</kbd> + <kbd>X</kbd> and then press <kbd>Y</kbd> to save the changes you made to the `.bashrc` file. Now close the Terminal.  
&nbsp;  
7. Open up a fresh Terminal and run the command `source ~/.bashrc` to put into effect the changes you made.  
&nbsp;  

### Creating an Alias in MacOS:  
1. Open the Terminal and cd to the home directory.  
&nbsp;  
2. Enter `ls -a` and check if there is the `.zshrc` file.    
&nbsp;  
3. If the `.zshrc` file does not exist, create it by running `touch .zshrc` in the Terminal.     
&nbsp;  
4. Now run the command `nano .zshrc` to open up the file in the nano editor.  
&nbsp;  
5. On a fresh line at the end of the file, add the line `alias cloe='python3 path/to/cloe.py'`. Make sure to replace `path/to/cloe.py` with the path to wherever you stored the `cloe.py` script on your system.  
&nbsp;  
6. Press <kbd>Cmd</kbd> + <kbd>X</kbd> and then press <kbd>Y</kbd> to save the changes you made to the `.zshrc` file. Now close the Terminal.  
&nbsp;  
7. Open up a fresh Terminal and run the command `source ~/.zshrc` to put into effect the changes you made.  
&nbsp;  

From now on, you can run your commands for Cloe like so:  
```commandline
$ cloe join <meeting-name>
```
___
