import csv

from config import gcdocs

node_id = 34589917
response = gcdocs.get_node_permissions(node_id=node_id)
results = response["results"]

with open("out/permissions.csv", "w") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["Assignee", "Type", "Permissions", "Members"])

    for result in results:
        permissions = gcdocs.get_result_value(
            response=result, key="permissions", property_name="permissions"
        )
        assignee = gcdocs.get_result_value(
            response=result, key="right_id", property_name="permissions"
        )
        assignee_type = gcdocs.get_result_value(
            response=result, key="type", property_name="permissions"
        )

        members = gcdocs.get_group_members(group=assignee, member_type=0)
        member_names = gcdocs.get_result_values(response=members, key="name")

        member = gcdocs.get_member(assignee)
        member_name = gcdocs.get_result_value(response=member, key="name")

        writer.writerow([member_name, assignee_type, permissions, member_names])
