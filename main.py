from gitlab_methods import add_members_to_group

# Configurations
ACCESS_TOKEN = "glpat-k8-G1TZbxYgq31U3rw2-" # access token

def main():
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}

    # payload to create a group
    # group_payload = {
    #     "name": "fun group 2",
    #     "path": "fun-group-2",
    #     "description": "This is is for fun",
    #     "visibility": "internal"
    # }
    # create_group(headers, group_payload)

    # add members to a group by id

    # group_payload for getting id
    # group_payload = {
    #     "name": "fun group 2"
    # }

    group_id = 44429 # or get_group_id(headers, group_payload)
    filename = "techlead_interns.csv" #csv file that consists group ids
    add_members_to_group(filename, headers, group_id, access_level=30)

