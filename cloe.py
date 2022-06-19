import os
import argparse
import json
import subprocess

# Relative path to the json file.
JSON_FILE_PATH = "zoom_meetings.json"


def load_meeting_data():
    # If the zoom_meetings.json file does not exist, create it.
    if not os.path.exists(os.path.join(os.getcwd(), JSON_FILE_PATH)):
        # Creating the file.
        with open(JSON_FILE_PATH, 'w') as f:
            print(f"{JSON_FILE_PATH} file created.")

        # Return an empty dictionary.
        return {}

    # Loading the JSON file containing the Zoom meeting information.
    with open(JSON_FILE_PATH, 'r') as json_file:
        meeting_data = json.load(json_file)

    return meeting_data


# Loading the meeting data from the zoom_meetings.json file. Only load once and it is available globally.
MEETING_DATA = load_meeting_data()


def dump_meeting_data_to_json():
    # Dump the dictionary into the json file.
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(MEETING_DATA, json_file, indent=4)


def add_meeting_entry(meeting_name: str,
                      meeting_id: str,
                      meeting_password: str = None) -> bool:
    """
    Function to add a new Zoom meeting entry into the zoom_meetings.json file.

    :param meeting_name: Name of the new Zoom meeting room
    :param meeting_id: Meeting ID for the new Zoom meeting
    :param meeting_password: Password for the new Zoom meeting: Optional
    :return: True if entry was added successfully
    """
    # Basic input validation. Checks if inputs are None or "".
    if meeting_name is False:
        print("Invalid value for meeting name parameter.")
        # Indicate operation failure.
        return False

    if meeting_id is False:
        print("Invalid value for meeting ID parameter.")
        # Indicate operation failure.
        return False

    # Check if the meeting_name contains any whitespaces. meeting names should not contain whitespaces.
    if ' ' in meeting_name:
        print("Meeting Names should not contain spaces. Use hyphens ('-') or underscores ('_') instead")

    """ If the meeting name already exists """
    if meeting_name in MEETING_DATA.keys():
        response = input(f"Meeting Name \"{meeting_name}\" already exists." 
                         "\nDo you want to overwrite the existing entry? [N/y]: ")

        if response.lower() != 'y':
            print("Add operation aborted.")
            return False
        else:
            print(f"Overwriting entry for meeting: {meeting_name}")

    # Creating a new dictionary entry for the meeting.
    MEETING_DATA[meeting_name] = {"meeting_id": meeting_id,
                                  "password": (meeting_password if meeting_password is not None else "")}

    # Dump the modified meeting data to the zoom_meetings.json file.
    dump_meeting_data_to_json()

    # Indicate successful operation.
    print(f"New meeting \"{meeting_name}\" added successfully.")
    return True


def remove_meeting_entry(meeting_name: str = None) -> bool:
    """
    Remove a Zoom meeting entry from the zoom_meetings.json file.

    :param meeting_name: meeting name of the entry to be removed
    :return: True if entry was removed successfully
    """
    # Validation.
    if meeting_name is None:
        print("Invalid meeting name parameter.")
        return False

    # If the meeting name doesn't exist.
    if meeting_name not in MEETING_DATA.keys():
        print(f"Meeting entry with name \"{meeting_name}\" does not exist.")
        return False

    # Removing the entry.
    MEETING_DATA.pop(meeting_name)

    # Dump modified meeting data into zoom_meetings.json file.
    dump_meeting_data_to_json()

    # Indicate successful operation.
    print(f"Meeting entry \"{meeting_name}\" removed successfully.")
    return True


def print_meeting_names():
    print("\n-> Stored Meeting entries: \n")

    # Print out all the meeting names.
    for index, meeting_name in enumerate(MEETING_DATA.keys()):
        print(f"{index}) {meeting_name}")

    # Spacing
    print("\n")


def join_meeting(meeting_name: str):
    # Getting the meeting ID.
    meeting_id = MEETING_DATA[meeting_name]["meeting_id"]

    # Getting the meeting password.
    meeting_password = MEETING_DATA[meeting_name]["password"]

    # Building the Zoom command. Only attach the password section if the meeting has a password.
    command = f'zoommtg://zoom.us/join?confno={meeting_id}' + (f'&pwd={meeting_password}' if meeting_password else "")

    # Running the shell command.
    process = subprocess.run(['xdg-open', command])


def main():
    # Initialize an argument parser.
    parser = argparse.ArgumentParser(description="Python script to open Zoom meetings in the Zoom Desktop Client from "
                                                 "the terminal.")

    # Adding arguments.
    parser.add_argument("action", type=str, help="The action to perform (ls, join, add, rm)")
    parser.add_argument("-n", "--mname", type=str, metavar="Meeting Name",
                        help="Name of the Zoom meeting")

    parser.add_argument("-I", "--mindex", type=int, metavar="Meeting Index",
                        help="Index of the Zoom meeting.")

    parser.add_argument("-i", "--mid", type=str, metavar="Meeting ID",
                        help="Meeting ID of the Zoom meeting")

    parser.add_argument("-p", "--mpw", type=str, metavar="Meeting Password",
                        help="Password to enter the Zoom meeting")

    # Parse the arguments.
    args = parser.parse_args()

    """ Determine the action """

    # Print the names of all the stored meeting entries.
    if args.action == "ls":
        print_meeting_names()

    # Join a meeting.
    elif args.action == "join":
        # Check if mname was provided and that mname exists in the meeting list.
        if args.mname and args.mname in MEETING_DATA.keys():
            join_meeting(meeting_name=args.mname)

        # Check if mindex was provided and that it is in the valid range.
        elif args.mindex and 0 <= args.mindex < len(MEETING_DATA.keys()):
            join_meeting(list(MEETING_DATA.keys())[args.mindex])

        # If both inputs were not valid.
        else:
            print("Invalid index or meeting name. Provide either --mname or --mindex to join a meeting.")

    # Add a new meeting entry.
    elif args.action == "add":
        # Validate that all the required arguments were provided.
        if all([args.mname, args.mid, args.mpw]):
            add_meeting_entry(meeting_name=args.mname, meeting_id=args.mid, meeting_password=args.mpw)
        else:
            print("Missing arguments for add command. Provide --mname, --mid and --mpw arguments.")

    # Remove a meeting entry.
    elif args.action == "rm":
        # Validate that the required argument was provided.
        if args.mname:
            remove_meeting_entry(meeting_name=args.mname)
        else:
            print("Missing arguments for rm command. Provide --mname argument.")

    # Invalid command
    else:
        print(f"\nUnknown command: {args.action}\n\n")


if __name__ == "__main__":
    main()
