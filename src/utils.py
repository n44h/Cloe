import platform
import subprocess


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

    def join(self) -> bool:
        """
        Join the Zoom meeting in the Zoom Desktop Client.

        :return: True if Zoom meeting join successfully.
        """

        # Building the Zoom command.
        command = f"zoommtg://zoom.us/join?confno={self.id}{f'&pwd={self.password}' if self.password else ''}"

        # Printing status message.
        print("\nLaunching Zoom Desktop Client...")

        # Execute the command.
        return_code = execute(command)

        # Analyze return code.
        if return_code == 0:
            print("\nSuccessfully joined Zoom meeting.\n")
            return True
        else:
            print("\nFailed to launch Zoom. Exiting with non-zero exit code.\n")
            return False

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

        # Number of Meetings stored in the MeetingDirectory instance.
        self.size = 0

    def add(self, name: str, m_id: str, password: str = None) -> (bool, str):
        """
        Create a Meeting instance and add it to the MeetingDirectory.

        :param name: name of the new meeting room
        :param m_id: meeting ID of the new meeting
        :param password: password of the new meeting, if it has one

        :return: True if meeting was added successfully
        """

        # Input validation. Check if the essential inputs are None or empty strings.
        if not name:
            return False, "\nInvalid value for meeting name parameter.\n"

        if not m_id:
            return False, "\nInvalid value for meeting ID parameter.\n"

        # Replace any whitespaces in the meeting name with '-'.
        if ' ' in name:
            name = name.replace(' ', '-')

        # Removing non-numeric characters from meeting_id.
        m_id = ''.join(c for c in m_id if c.isdigit())

        # Check if the meeting name already exists.
        if name in self.meeting_names:
            # If the meeting name already exists, get user confirmation to update existing meeting data.
            print(f"\nA meeting with the name \"{name}\" already exists.")
            response = input("Do you want to update the existing meeting entry? [N/y]: ")

            # If the user chooses to abort the operation.
            if response.lower() not in ['y', 'yes']:
                return False, "\nOperation aborted.\n"

            # Update the meeting.
            return self.update(name, name, m_id, password)

        else:
            # Adding the new meeting.
            self.meeting_names.append(name)
            self.meetings.append(Meeting(name, m_id, password))

            return True, f"\nAdded new meeting \"{name}\".\n"

    def update(self, old_name, new_name, new_id, new_password) -> bool:
        """
        Update an existing Meeting instance in the MeetingDirectory.

        :param old_name: the old name of the meeting
        :param new_name: new name of the meeting
        :param new_id: new ID of the meeting
        :param new_password: new password of the meeting, if it has one

        :return: True if meeting was updated successfully
        """

        # Input validation. Check if the essential inputs are None or empty strings.
        if not new_name:
            print("\nInvalid value for meeting name.\n")
            return False

        if not new_id:
            print("\nInvalid value for meeting ID.\n")
            return False

        # Replace any whitespaces in the meeting name with '-'.
        if ' ' in new_name:
            new_name = new_name.replace(' ', '-')
            print("\nReplaced whitespaces in meeting name with '-'.\n")

        # Removing non-numeric characters from meeting_id.
        new_id = ''.join(c for c in new_id if c.isdigit())

        # Check if the meeting name exists.
        if new_name not in self.meeting_names:
            print(f"\nMeeting with name \"{new_name}\" does not exist.\n")
            return False

        else:
            # Get index of the meeting.
            idx = self.meeting_names.index(old_name)

            # Updating the meeting.
            self.meeting_names[idx] = new_name
            self.meetings[idx] = Meeting(new_name, new_id, new_password)

            return True

    def remove(self, name) -> bool:
        """
        Remove a meeting from the MeetingDirectory.

        :param name: name of the meeting to be removed

        :return: True if meeting was removed successfully
        """

        # Validation.
        if name is None:
            print("\nMeeting entry cannot be None.\n")
            return False

        # If the meeting name doesn't exist.
        if name not in self.meeting_names:
            print(f"\nMeeting entry \"{name}\" does not exist.\n")
            return False

        # Confirmation prompt.
        confirm = input(f"\nConfirm that you want to remove \"{name}\"? [N/y]: ")

        # If user did not confirm operation.
        if confirm.lower() not in ['y', 'yes']:
            print("\nRemove operation aborted.\n")
            return False

        # If user confirmed remove operation.
        else:
            # Get the index of the meeting.
            idx = self.meeting_names.index(name)

            # Removing the entry.
            self.meeting_names.pop(idx)
            self.meetings.pop(idx)

            return True

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

        :param item: index or key

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
