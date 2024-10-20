import os

# Function to recursively find all files with '.approved.' in their name
def find_approved_files(directory):
    approved_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if '.approved.' in file:
                approved_files.append(os.path.join(root, file))
    return approved_files

# Read the contents of approvedfiles.log and create a set of paths
def read_approved_files_log(log_path):
    with open(log_path, 'r') as f:
        approved_files_log = set(line.strip() for line in f if line.strip())
    return approved_files_log

# Compare the found files with the ones in the log
def compare_files(found_files, log_files):
    not_in_log = [file for file in found_files if file not in log_files]
    return not_in_log

def main():
    # Specify the directory to search and the log file path
    directory_to_search = '.'  # Adjust if needed
    log_file_path = 'approvedfiles.log'

    # Find approved files and read log file
    found_files = find_approved_files(directory_to_search)
    log_files = read_approved_files_log(log_file_path)

    # Compare the lists and output the result
    missing_files = compare_files(found_files, log_files)

    if missing_files:
        print("The following files are not in the approved log:")
        for file in missing_files:
            print(file)
    else:
        print("All found approved files are present in the log.")

if __name__ == "__main__":
    main()