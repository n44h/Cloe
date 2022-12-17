import platform
import subprocess


FAILURE_MESSAGE = """
Failed to launch Zoom.
Please ensure that you have:
    1. installed the latest version of the Zoom Desktop Client
    2. logged into the Zoom Desktop Client
    3. provided a valid meeting ID (and correct password, if required)
"""


def execute(command: str = None) -> int | None:
    """
    Function to execute commands in the shell.

    :param command: command to execute in the shell.
    :return: process return code; 0 indicates successful command execution.
    """

    # Checking for empty command.
    if not command:
        return None

    # Get the operating system name.
    host_os = platform.system().lower()

    if "linux" in host_os:
        # Running the shell command for Linux.
        process = subprocess.run(['xdg-open', command])

    elif "darwin" in host_os:
        # Running the shell command for macOS.
        process = subprocess.run(['open', command])

    elif "windows" in host_os:
        # Running the shell command for Windows.
        process = subprocess.run(['start', command])

    else:
        print("\nUnrecognized Operating System.")
        return 1

    # Return the process' return code. Return code 0 indicates successful execution.
    return process.returncode


class Placeholder:
    """
    Class to serve as a placeholder value for the Meeting class attribute "password" when there is no meeting password.

    This is done because NoneType cannot be used as a placeholder in the Meeting class for semantic reasons.
    """

    def __bool__(self):
        return False

    def __str__(self):
        return "-nil-"


class Meeting:
    def __init__(self, name: str, m_id: str, password: str = None):
        self.name = name
        self.id = m_id
        self.password = password if password is not None else Placeholder()

    def update(self,
               name: str = None,
               m_id: str = None,
               password: str | None = Placeholder()):

        self.name = name if name else self.name
        self.id = m_id if m_id else self.id

        """
        If password is a NoneType instance     ->  set self.password = Placeholder() instance ; Remove password

        If password is a Placeholder instance  ->  set self.password = self.password          ; Keep old password

        If password is a str instance          ->  set self.password = password               ; Update to new password
        """
        if password is None:
            self.password = Placeholder()

        elif isinstance(password, str):
            self.password = password

    def __eq__(self, other):
        # Meeting names are unique. Check if the 2 Meeting instances have the same meeting name.
        return self.name == other.name

    def __str__(self):
        return f"Meeting(name: {self.name}, id: {self.id}, password required: {bool(self.password)})"


class MeetingDirectory:
    def __init__(self):
        # List of meeting names.
        self.meeting_names = []

        # List of Meeting instances.
        self.meetings = []

    @property
    def size(self):
        return len(self.meetings)

    def add(self, name: str, m_id: str, password: str = None) -> (bool, str):
        """
        Create a Meeting instance and add it to the MeetingDirectory.

        :param name: name of the new meeting room
        :param m_id: meeting ID of the new meeting
        :param password: password of the new meeting, if it has one

        :return: True if meeting was added successfully, and a message
        """

        # Check if meeting name is an empty string or None.
        if not name:
            return False, "Invalid meeting name"

        # Replace any whitespaces in the meeting name with '-'.
        if ' ' in name:
            name = name.replace(' ', '-')

        # Removing '-'s from the meeting id.
        if m_id is not None:
            m_id = m_id.replace('-', '')

        # Check if meeting id is an empty string or None.
        if not m_id:
            return False, "Invalid meeting ID"

        # Check if the meeting name already exists.
        if name in self.meeting_names:
            # If the meeting name already exists, get user confirmation to update existing meeting data.
            print(f"\nA meeting with the name \"{name}\" already exists.")
            response = input(" > Do you want to update the existing meeting entry? [N/y]: ")

            # If the user chooses to abort the operation.
            if response.lower() not in ['y', 'yes']:
                return False, "Add operation aborted"

            # Update the meeting.
            return self.update(name, m_id, password)

        else:
            # Adding the new meeting.
            self.meeting_names.append(name)
            self.meetings.append(Meeting(name, m_id, password))

            return True, f"Added new meeting \"{name}\""

    def update(self, new_name, new_id, new_password, old_name: str = None) -> (bool, str):
        """
        Update an existing Meeting instance in the MeetingDirectory.

        :param old_name: the old name of the meeting
        :param new_name: new name of the meeting
        :param new_id: new ID of the meeting
        :param new_password: new password of the meeting, if it has one

        :return: True if meeting was updated successfully, and a message
        """

        # Check if new meeting name is an empty string or None.
        if not new_name:
            return False, "Invalid meeting name"

        # Replace any whitespaces in the new meeting name with '-'.
        if ' ' in new_name:
            new_name = new_name.replace(' ', '-')

        # Removing '-'s from the new meeting id.
        if new_id is not None:
            new_id = new_id.replace('-', '')

        # Check if new meeting id is an empty string or None.
        if not new_id:
            return False, "Invalid meeting ID"

        # If the old name is None, assign it the value of new name (this is inconsequential).
        if not old_name:
            old_name = new_name

        # Check if the old meeting name exists in the meeting directory.
        if old_name in self.meeting_names:
            # Get index of the meeting.
            idx = self.meeting_names.index(old_name)

            # Updating the meeting.
            self.meeting_names[idx] = new_name
            self.meetings[idx] = Meeting(new_name, new_id, new_password)

            return True, f"Updated meeting \"{new_name}\""

        else:
            return False, f"Meeting with name \"{old_name}\" does not exist"

    def remove(self, name) -> (bool, str):
        """
        Remove a meeting from the MeetingDirectory.

        :param name: name of the meeting to be removed

        :return: True if meeting was removed successfully, and a message
        """

        # Validation.
        if name is None:
            return False, "Meeting name cannot be None"

        # If the meeting name doesn't exist.
        if name not in self.meeting_names:
            return False, f"Meeting \"{name}\" does not exist"

        # Confirmation prompt.
        confirm = input(f"\n > Confirm that you want to remove \"{name}\"? [N/y]: ")

        # If user confirmed the remove operation.
        if confirm.lower() in ['y', 'yes']:
            # Get the index of the meeting.
            idx = self.meeting_names.index(name)

            # Removing the entry.
            self.meeting_names.pop(idx)
            self.meetings.pop(idx)

            return True, f"Removed meeting \"{name}\""

        # If user did not confirm the remove operation.
        else:
            return False, "Remove operation aborted"

    def join(self, key: str | int) -> (bool, str):
        """
        Join the Zoom meeting in the Zoom Desktop Client.

        :return: True if the meeting is joined successfully.
        """

        # Check if key is None.
        if key is None:
            return False, "Invalid key"

        # Get the meeting instance.
        # Regardless of whether the key is the meeting name or index, the code below will work.
        # See: MeetingDirectory.__getitem__() to understand how this is handled.
        try:
            meeting = self[key]
        except KeyError:
            return False, f"Meeting name \"{key}\" does not exist"
        except IndexError:
            return False, f"Invalid meeting index {key}"

        # Building the Zoom command.
        command = f"zoommtg://zoom.us/join?confno={meeting.id}{f'&pwd={meeting.password}' if meeting.password else ''}"

        # Execute the command.
        return_code = execute(command)

        # Analyze return code.
        if return_code == 0:
            return True, "Launched Zoom Meeting Client"

        else:
            return False, FAILURE_MESSAGE

    @staticmethod
    def quick_join(m_id: str, password: str = None) -> (bool, str):
        """
        Quick join a meeting without saving it to Cloe.

        :param m_id: meeting ID
        :param password: meeting password, if one is required

        :return: True if the meeting was joined successfully
        """

        # Removing '-'s from the meeting id.
        if m_id is not None:
            m_id = m_id.replace('-', '')

        if not m_id:
            return False, "Invalid meeting ID parameter"

        # Building the Zoom command.
        command = f"zoommtg://zoom.us/join?confno={m_id}{f'&pwd={password}' if password else ''}"

        # Execute the command.
        return_code = execute(command)

        # Analyze return code.
        if return_code == 0:
            return True, "Launched Zoom Desktop Client"

        else:
            return False, FAILURE_MESSAGE

    def get_meetings(self):
        return self.meetings

    def is_valid_index(self, idx):
        """
        Checks if an index is valid, i.e. within range 0 to (size-1).

        :param idx: index value to check

        :return: True if index is valid
        """
        return -1 < idx < self.size

    def __len__(self):
        return self.size

    def __contains__(self, meeting_name):
        return meeting_name in self.meeting_names

    def __getitem__(self, item):
        """
        Returns Meeting instance with corresponding key or at specified index.

        item can be a numeric index value or a key value (meeting name)

        :param item: meeting index or name

        :return: Meeting instance
        """

        if isinstance(item, int):
            # Raise an IndexError if the index is out of bounds.
            if item < 0 or item >= self.size:
                raise IndexError(f"{item} is out of range {self.size}.")

            return self.meetings[item]

        else:
            # Raise a KeyError if the key (meeting name) does not exist.
            if item not in self.meeting_names:
                raise KeyError(f"key {item} does not exist.")

            return self.meetings[self.meeting_names.index(item)]

    def __str__(self):
        return f"MeetingRegister(number of meetings = {self.size})"
