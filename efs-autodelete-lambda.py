import os
import time
import shutil

def lambda_handler(event, context):
    folders_count = 0
    files_count = 0

    # specify the path
    path = "/mnt/efs"
    # specify the days
    days = 30

    # converting days to seconds
    # time.time() returns current time in seconds
    seconds = time.time() - (days * 24 * 60 * 60)

    # checking whether the file is present in path or not
    if os.path.exists(path):
        # iterating over each and every folder and file in the path
        for root_folder, folders, files in os.walk(path):

            for file in files:
                # file path
                file_path = os.path.join(root_folder, file)
                if seconds > get_file_or_folder_age(file_path):
                    files_count += 1
                    remove_file(file_path)

    else:

        print(f"{path} not found")

    print("Total files:", files_count)
def get_file_or_folder_age(path):

	# getting ctime of the file/folder
	# time will be in seconds
	ctime = os.stat(path).st_ctime

	# returning the time
	return ctime

def remove_file(path):

	# removing the file
	if not os.remove(path):

		# success message
		print(f"{path} deleted successfully")

	else:

		# failure message
		print(f"Unable to delete the {path}")
