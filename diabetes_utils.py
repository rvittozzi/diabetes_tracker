

def get_last_check_time():
    try:
        with open("last_check_time.txt", "r") as file:
            last_check_time = file.read()
            return last_check_time
    except FileNotFoundError:
        # Return a default value if the file doesn't exist or there's an issue
        return None
