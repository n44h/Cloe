import os
import argparse
import dill as pkl

from utils import Meeting, MeetingDirectory


# Cloe root directory absolute path.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to the meeting data file.
MEETING_DIR_PKL_FILENAME = "meeting_directory.pkl"

# Getting parent path and joining it with the file name.
MEETING_DIR_PKL_FILEPATH = os.path.join(ROOT_DIR, "res", MEETING_DIR_PKL_FILENAME)

# MeetingDirectory instance.
MEETING_DIR = MeetingDirectory()


def load_meeting_data() -> MeetingDirectory:
    # If the file does not exist.
    if not os.path.exists(MEETING_DIR_PKL_FILEPATH):
        # Creating the file.
        with open(MEETING_DIR_PKL_FILEPATH, 'wb') as f:
            pass

        # Print operation message.
        print(f"Create file {MEETING_DIR_PKL_FILENAME}.")

        # Return a new MeetingDirectory instance.
        return MeetingDirectory()

    # If the file is empty.
    elif os.path.getsize(MEETING_DIR_PKL_FILEPATH) == 0:
        # Return a new MeetingDirectory instance.
        return MeetingDirectory()

    # If the file exists, and it is not empty, load the MeetingDirectory instance.
    else:
        # Loading the file containing the serialized MeetingDirectory instance.
        with open(MEETING_DIR_PKL_FILEPATH, 'rb') as f:
            meeting_directory = pkl.load(f)

        return meeting_directory


def dump_meeting_data(meeting_dir: MeetingDirectory) -> None:
    # Dump the meeting directory to file.
    with open(MEETING_DIR_PKL_FILEPATH, "wb") as f:
        pkl.dump(meeting_dir, f)


def add_meeting(name: str, m_id: str, password: str = None) -> bool:
    """
    Add a meeting to Cloe.

    :param name: name of the new meeting room
    :param m_id: meeting ID of the new meeting
    :param password: password of the new meeting, if one is required

    :return: True if meeting was added successfully
    """

    success, msg = MEETING_DIR.add(name, m_id, password)

    if success:
        # Serialize the updated meeting directory to file.
        dump_meeting_data(MEETING_DIR)

        # Print operation success message.
        print(msg)
        return True

    else:
        # Print operation failure message.
        print(msg)
        return False


def remove_meeting(name: str = None) -> bool:
    """
    Remove a meeting from Cloe.

    :param name: name of the meeting to be removed

    :return: True if meeting was removed successfully
    """

    if MEETING_DIR.remove(name):
        # Print operation success message.
        print(f"\nRemoved meeting \"{name}\".\n")
        return True

    else:
        # Print operation failure message.
        print(f"\nCould not remove meeting \"{name}\".\n")
        return False


def join_meeting(key: str | int) -> bool:
    """
    Join a saved meeting using the meeting name or the meeting's list index.

    :param key: the meeting name or index of the meeting to join.

    :return: True if the meeting was joined successfully
    """

    # Check if key is None.
    if key is None:
        return False

    # Join the meeting. Regardless of whether the key is the meeting name or index, the code below will work.
    # See: MeetingDirectory.__getitem__() to understand how this is handled.
    return_code = MEETING_DIR[key].join()

    # Print success message if meeting was joined successfully.
    if return_code == 0:
        print("\nSuccessfully joined Zoom meeting.\n")
        return True

    # Print failure message.
    else:
        print("\nFailed to launch Zoom."
              "\nPlease ensure that you:"
              "\n  1. have installed the latest version of the Zoom Desktop Client"
              "\n  2. logged into the Zoom Desktop Client\n")

        return False


def quick_join_meeting(m_id: str, password: str = None) -> bool:
    """
    Join a meeting without saving it to Cloe.

    :param m_id: meeting ID
    :param password: meeting password, if one is required

    :return: True if the meeting was joined successfully
    """

    if not m_id:
        print("\nInvalid value for meeting ID parameter.\n")
        return False

    # Removing non-numeric characters from meeting_id.
    m_id = ''.join(c for c in m_id if c.isdigit())

    # Create a temporary Meeting instance.
    meeting = Meeting("", m_id, password)

    # Join the meeting.
    return_code = meeting.join()

    # Print success message if meeting was joined successfully.
    if return_code == 0:
        print("\nSuccessfully joined Zoom meeting.\n")
        return True

    # Print failure message.
    else:
        print("\nFailed to launch Zoom."
              "\nPlease ensure that you have:"
              "\n  1. installed the latest version of the Zoom Desktop Client"
              "\n  2. logged into the Zoom Desktop Client\n"
              "\n  3. provided a valid meeting ID (and correct password, if required)\n")

        return False


def print_meeting_names(only_names: bool = False, show_passwords: bool = False):
    print("\n-> Saved Meetings: \n")

    # Print out all the meetings.
    for index, meeting in enumerate(MEETING_DIR.get_meetings()):

        # Print meeting name.
        print(f"{index}) {meeting.name}")

        # If only_names is False, print meeting ID.
        if not only_names:
            print(f"\n\tMeeting ID: {meeting.id}")

            # If show_passwords is True, print meeting passwords.
            if show_passwords:
                print(f"\n\tPassword  : {meeting.password}\n")

    # Spacing
    print("\n")


def main():
    # Initialize an argument parser.
    parser = argparse.ArgumentParser(description="Open Zoom meetings in the Zoom Desktop Client using the CLI.")

    # Adding arguments.
    parser.add_argument("command",
                        type=str,
                        required=True,
                        choices=['ls', 'list', 'join', 'add', 'rm', 'remove'],
                        help="The command to perform (ls, join, add, rm)"
                        )

    parser.add_argument("pos-args",
                        dest="positional",
                        type=str,
                        required=False,
                        nargs="?",
                        help="Positional arguments depending on the command."
                        )

    parser.add_argument("-n", "--only-names",
                        dest="only_name",
                        type=bool,
                        required=False,
                        action='store_true',
                        metavar="List only meeting names",
                        help="Flag to indicate only meeting names must be shown when listing saved meetings"
                        )

    parser.add_argument("-p", "--show-passwords",
                        dest="show_passwords",
                        type=bool,
                        required=False,
                        action='store_true',
                        metavar="List meeting passwords",
                        help="Flag to indicate whether passwords must be shown when listing saved meetings")

    # Parse the arguments.
    args = parser.parse_args()

    # Get number of positional arguments.
    num_args = len(args.positional)

    # Assess the command.
    # 1. List saved meetings.
    if args.command in ["ls", "list"]:
        print_meeting_names(args.only_names, args.show_passwords)

    # 2. Join a meeting.
    elif args.command == "join":
        if num_args == 1:
            # Generate the possible variables positional[0] could be.
            name = args.positional[0]
            m_id = args.positional[0]
            try:
                index = int(args.positional[0])
            except ValueError:
                index = -1

            # 2.1 Join a saved meeting using meeting name.
            # Check if the meeting name exists.
            if name in MEETING_DIR:
                join_meeting(name)

            # 2.2 Join a saved meeting using meeting index.
            # Check if the index is valid.
            elif MEETING_DIR.is_valid_index(index):
                join_meeting(index)

            # 2.3 Quick join a meeting with the meeting ID.
            else:
                quick_join_meeting(m_id=m_id)

        # 2.4 Quick join a meeting with meeting ID and password.
        elif num_args == 2:
            quick_join_meeting(m_id=args.positional[0], password=args.positional[1])

        # Invalid number of arguments (0 or >2).
        else:
            print(f"\nError: \"join\" command expects 1 or 2 arguments but received {num_args}\n")

    # 3. Add a new meeting.
    elif args.command == "add":
        # Check if correct number of arguments were provided.
        if num_args == 2:
            add_meeting(name=args.positional[0], m_id=args.positional[1])

        elif num_args == 3:
            add_meeting(name=args.positional[0], m_id=args.positional[1], password=args.positional[2])

        else:
            print(f"\nError: \"add\" command expects 2 or 3 arguments but received {num_args}\n")

    # 4. Remove a meeting.
    elif args.command in ["rm", "remove"]:
        # Check if correct number of arguments were provided.
        if num_args == 1:
            remove_meeting(name=args.positional[0])

        else:
            print(f"\nError: \"remove\" command expects 1 argument but received {num_args}\n")

    # Invalid command
    else:
        print(f"\nUnknown command: {args.command}\n\n")


if __name__ == "__main__":
    main()
