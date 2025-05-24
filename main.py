from gitlab_methods import (
    add_members_to_group,
    check_file_in_repo,
    get_all_groups,
    get_all_users_from_group,
    remove_group,
    remove_projects,
    update_access_level,
    update_project_access_level,
)
import csv

# Configurations
ACCESS_TOKEN = "glpat-ySGQMMC8sdPESB2yWU2z"  # access token


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

    group_id = 44429  # or get_group_id(headers, group_payload)

    # adding to the group

    # filename = "interns.csv" #csv file that consists group ids
    # print("started adding group: ")
    # add_members_to_group(filename, headers, group_id, access_level=40)

    # project_id = 17159
    # # updating user access level
    # users = []
    # with open('vagdevi.csv', mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         users.append(row)
    # # update_access_level(group_id, users, headers, 40)

    # update_project_access_level(project_id, users, headers, 40)

    # removing projects from the group

    # group_list = get_all_groups(headers, group_id)
    # remove_projects(headers, group_list)

    project_id = 44429
    users = get_all_users_from_group(headers, project_id)

    with open("output.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "username", "profile_readme", "profile_card"])

    for user in users:
        project_path = f"{user['username']}/{user['username']}"
        file_path = "README.md"
        profile_readme_result = check_file_in_repo(headers, project_path, file_path)
        project_path = "soai2025/profiles"
        file_path = f"profiles/{user['username']}.md"
        profile_card_result = check_file_in_repo(headers, project_path, file_path)
        with open("output.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    user["name"],
                    user["username"],
                    profile_readme_result,
                    profile_card_result,
                ]
            )


if __name__ == "__main__":
    main()
