import hashlib
import yaml
import json
import numpy as np
import requests

from bisect import bisect_left
from pprint import pprint


base_url = "https://api.pwnedpasswords.com/range/"          # Pwnedpassword API URL (we will append the partial hash)
headers = {'user-agent': 'pwnedpassword-checker-python'}    # Arbitrary user-agent name; otherwise request rejected


# Basic search function, but first converts list to array
# returns -1 if not found, otherwise index in list
def search(look_up_key, keys_list):
    keys_only_array = np.asarray(keys_list)
    i = bisect_left(keys_only_array, look_up_key)
    if i != len(keys_only_array) and keys_only_array[i] == look_up_key:
        return i

    return -1


# Do an API lookup for the given password
# return -2 if API server response is not OK (this should not happen)
# return -1 if password is not found on server (this is what you want -- means password is not compromised)
# else returns num occurrences of password in online dataset (see API documentation for more info)
def check_api_for_password(pw):
    # Hash and tweak password
    pass_sha1 = hashlib.sha1(pw.encode()).hexdigest().upper()   # Hash upper-cased to match API return values
    pass_sha1_truncated = pass_sha1[0:5]                        # API takes only the first 5 chars (k-anonymity)

    # Get the API response
    full_url = base_url + pass_sha1_truncated
    api_response = requests.get(full_url, headers=headers)

    # Check valid response (Note there is no rate limit for pwnedpassword ApI)
    if api_response.status_code != requests.codes.ok:
        print("error: status code: " + api_response.status_code)
        print("error response: " + api_response.text)
        return -2

    # Parse response
    # Response is of form <hash_omitting_first_five chars>:<num_occurrences>\n
    # Convert to string tuples of form [[partial_hash, num_occurences]]
    # Hash omits the first five characters (the chars we used to query)
    response_hashes = [x.strip().split(":") for x in api_response.text.split("\n")]

    # Check for the full SHA1 (we strip first 5 chars) to match server responses
    # List comprehension to get only the first element (the partial hash) of each tuple
    search_look_up = search(pass_sha1[5:], [x[0] for x in response_hashes])
    if search_look_up == -1:
        return -1                                               # not found, all OK

    return int(response_hashes[search_look_up][1])              # else return the number of occurrences in dataset


if __name__ == '__main__':
    # Read config file for dashlane pw file
    dashlane_file = ""
    with open("example_config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        dashlane_file = cfg['dashlane_file']

    if dashlane_file == "":
        print("You need to update your config file to have your own dashlane.json file\n"
              "From dashlane, export your passwords in json format. Then specify that file location "
              "in the config.yml file")
        exit(1)
    else:
        print("using file: " + dashlane_file)

    # For all passwords in the dashlane file, check the API and report back
    try:
        with open(dashlane_file) as f:
            data = json.load(f)
            passwords = data["AUTHENTIFIANT"]       # passwords portion of dashlane json export
            index = 0
            for i in range(len(passwords)):
                index = i

                curr = passwords[i]
                curr_pw = curr['password']

                check_api_response = check_api_for_password(curr_pw)
                if check_api_response == -2:
                    print("stopping at index %d", i)
                    break
                elif check_api_response == -1:
                    continue
                else:
                    print("password found: " + curr_pw)
                    print(check_api_response)
                    pprint(curr)

        print("finished at index ", index)

    except FileNotFoundError:
        print("Your dashlane.json file is invalid. Update your config file")
