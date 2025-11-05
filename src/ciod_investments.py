import csv

from config import gcdocs


def split_name(full_name: str) -> tuple[str, str]:
    names = full_name.split()
    first_name = names[0]
    last_name = " ".join(names[1:])
    return (first_name, last_name)


with open("in/Manager Workspaces.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Project Manager
        manager_name = row["Project Manager"]
        first_name, last_name = split_name(manager_name)
        response = gcdocs.get_users(
            where_first_name=first_name, where_last_name=last_name
        )
        manager_id = gcdocs.get_result_value(response=response, key="id")

        # Business Sponsor
        sponsor_name = row["Business Sponsor"]
        sponsor_id = None
        if sponsor_name:
            first_name, last_name = split_name(sponsor_name)
            response = gcdocs.get_users(
                where_first_name=first_name, where_last_name=last_name
            )
            sponsor_id = gcdocs.get_result_value(response=response, key="id")

        # CIOD Delivery Director
        director_name = row["CIOD Delivery Director"]
        director_id = None
        if director_name:
            first_name, last_name = split_name(director_name)
            response = gcdocs.get_users(
                where_first_name=first_name, where_last_name=last_name
            )
            director_id = gcdocs.get_result_value(response=response, key="id")

        # Client Group / Branch Code
        group_name = row["Client Group / Branch Code"]
        group_id = None
        if group_name:
            response = gcdocs.get_group(name=group_name)
            group_id = gcdocs.get_result_value(response=response, key="id")

        # # Initial Target Date
        # initial_date = row["Initial Target Date"]
        # if initial_date:
        #     initial_date += "T00:00:00"

        # # Revised Target Date
        # revised_date = row["Revised Target Date"]
        # if revised_date:
        #     revised_date += "T00:00:00"

        category_data = {
            "52250339": {
                "52250339_2": row["Investment Type"],
                "52250339_3": row["Project name"],
                "52250339_4": row["Description"],
                "52250339_5": row["Status"],
                "52250339_7": row["Revised Target Date"],
                "52250339_9": row["Revised Target Date"],
                "52250339_10": row["Health"],
                "52250339_11": sponsor_id,
                "52250339_12": group_id,
                "52250339_13": director_id,
                "52250339_14": manager_id,
                "52250339_15": row["Issues / Blockers"],
                "52250339_16": row["Achieved Last Period"],
                "52250339_17": row["Planned For Next Period"],
                "52250339_21": row["Additional Information"],
                "52250339_22": row["Entered in EPM"],
                "52250339_23": row["Comments"],
            }
        }

        # response = gcdocs.get_workspace_by_type_and_name(
        #     type_id=139, name=row["Project name"]
        # )
        # print(response)
        # continue

        gcdocs.create_workspace(
            workspace_template_id=52101324,
            workspace_name=row["Project name"],
            workspace_description=row["Description"],
            workspace_type=139,
            category_data=category_data,
            parent_id=52102181,
        )
