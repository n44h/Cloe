import os
import sys
import argparse
import dill as pkl
from pathlib import Path
from utils import MeetingDirectory


# Cloe root directory absolute path.
ROOT_DIR = Path(__file__).absolute().parents[1]

# Absolute path to the resource directory.
RESOURCE_DIR = ROOT_DIR / "res"

# File path tot the meeting directory serialized object file
MEETING_DIR_PKL_FILE = RESOURCE_DIR / "cloe.mtgdir"


def load_meeting_data() -> MeetingDirectory:
    # If the file does not exist.
    if not os.path.exists(MEETING_DIR_PKL_FILE):
        # Create the directory.
        os.makedirs(RESOURCE_DIR, exist_ok=True)

        # Creating the file.
        with open(MEETING_DIR_PKL_FILE, 'wb') as f:
            pass

        # Print operation message.
        print(f"Created file {MEETING_DIR_PKL_FILE}.")

        # Return a new MeetingDirectory instance.
        return MeetingDirectory()

    # If the file is empty.
    elif os.path.getsize(MEETING_DIR_PKL_FILE) == 0:
        # Return a new MeetingDirectory instance.
        return MeetingDirectory()

    # If the file exists, and it is not empty, load the MeetingDirectory instance.
    else:
        # Loading the file containing the serialized MeetingDirectory instance.
        with open(MEETING_DIR_PKL_FILE, 'rb') as f:
            meeting_directory = pkl.load(f)

        return meeting_directory


def dump_meeting_data(meeting_dir: MeetingDirectory) -> None:
    # Dump the meeting directory to file.
    with open(MEETING_DIR_PKL_FILE, "wb") as f:
        pkl.dump(meeting_dir, f)


def list_meetings(meeting_directory: MeetingDirectory, show_ids: bool = False, show_passwords: bool = False):
    print("\n> Saved Meetings:")

    # Check if meeting directory is empty.
    if len(meeting_directory) == 0:
        print("-- No saved meetings --\n")
        return

    # Print out all the meetings.
    for index, meeting in enumerate(meeting_directory.get_meetings()):

        # Print meeting name.
        print(f"{index}) {meeting.name}")

        # If show_ids or show_passwords is True, print meeting IDs.
        if show_ids or show_passwords:
            print(f"\tMeeting ID : {meeting.id}")

        # If show_passwords is True, print meeting passwords.
        if show_passwords:
            print(f"\tPassword   : {meeting.password}")

        # Spacing only for long formats.
        if show_ids or show_passwords:
            print()

    # End spacing for short format
    if not show_ids and not show_passwords:
        print()


def main():
    # Load the serialized meeting directory from file.
    meeting_directory = load_meeting_data()

    # Set default values for operation success and msg.
    op_success, msg = False, None

    # Initialize an argument parser.
    parser = argparse.ArgumentParser(description="Open Zoom meetings in the Zoom Desktop Client using the CLI.")

    # Adding arguments.
    parser.add_argument("command",
                        type=str,
                        nargs="?",
                        const=1,
                        choices=['join', 'add', 'remove', 'list', 'reset'],
                        help="Action to execute",
                        default="list"
                        )

    parser.add_argument("positional",
                        type=str,
                        nargs="*",
                        help="Positional arguments depending on the command."
                        )

    parser.add_argument("-q", "--quick-join",
                        dest="quick_join",
                        required=False,
                        action='store_true',
                        help="Flag used to quick join a meeting"
                        )

    parser.add_argument("-i", "--show-ids",
                        dest="show_ids",
                        required=False,
                        action='store_true',
                        help="Flag to indicate whether meetings IDs must be shown when listing saved meetings"
                        )

    parser.add_argument("-p", "--show-passwords",
                        dest="show_passwords",
                        required=False,
                        action='store_true',
                        help="Flag to indicate whether passwords must be shown when listing saved meetings")

    # Parse the arguments.
    args = parser.parse_args()

    # Get number of positional arguments.
    num_args = len(args.positional) if args.positional is not None else 0

    # Assess the command.
    # 1. List saved meetings.
    if args.command == "list":
        list_meetings(meeting_directory, args.show_ids, args.show_passwords)
        op_success = True

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
            if name in meeting_directory:
                op_success, msg = meeting_directory.join(name)

            # 2.2 Join a saved meeting using meeting index.
            # Check if the index is valid.
            elif meeting_directory.is_valid_index(index):
                op_success, msg = meeting_directory.join(index)

            # 2.3 Quick join a meeting with the meeting ID.
            elif args.quick_join:
                op_success, msg = meeting_directory.quick_join(m_id=m_id)

            else:
                op_success, msg = False, f"Invalid meeting name or index \"{args.positional[0]}\""

        # 2.4 Quick join a meeting with meeting ID and password.
        elif num_args == 2:
            op_success, msg = meeting_directory.quick_join(m_id=args.positional[0], password=args.positional[1])

        # Invalid number of arguments (0 or >2).
        else:
            msg = f"Error: \"join\" command expects 1 or 2 arguments but received {num_args}"

    # 3. Add a new meeting.
    elif args.command == "add":
        # Check if correct number of arguments were provided.
        if num_args == 2:
            op_success, msg = meeting_directory.add(name=args.positional[0],
                                                    m_id=args.positional[1])

        elif num_args == 3:
            op_success, msg = meeting_directory.add(name=args.positional[0],
                                                    m_id=args.positional[1],
                                                    password=args.positional[2])

        else:
            msg = f"Error: \"add\" command expects 2 or 3 arguments but received {num_args}"

    # 4. Remove a meeting.
    elif args.command == "remove":
        # Check if correct number of arguments were provided.
        if num_args == 1:
            op_success, msg = meeting_directory.remove(name=args.positional[0])

        else:
            msg = f"Error: \"remove\" command expects 1 argument but received {num_args}"

    # 5. Clear all saved meetings.
    elif args.command == "reset":
        # Confirmation prompt.
        confirm = input(f"\n > Confirm that you want to remove all saved meetings from Cloe? [N/y]: ")

        # If user confirmed the clear operation.
        if confirm.lower() in ['y', 'yes']:
            # Reinitialize meeting directory to fresh MeetingDirectory instance.
            meeting_directory = MeetingDirectory()
            op_success = True
            msg = "Cleared all saved meetings"

        # If user did not confirm the clear operation.
        else:
            op_success = False
            msg = "Clear operation aborted"

    # Invalid command
    else:
        msg = f"Unknown command: {args.command}"

    # Print message and serialize updated meeting directory.
    if msg:
        print(f"{msg}\n")

    if op_success:
        # Serialize the updated meeting directory to file.
        dump_meeting_data(meeting_directory)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
