import csv

from config import gcdocs

root_id = 33266495

provinces = {
    "Alberta": "AB - Alberta | Alberta",
    "British Columbia": "BC - British Columbia | Colombie-Britannique",
    "Manitoba": "MB - Manitoba | Manitoba",
    "New Brunswick": "NB - New Brunswick | Nouveau-Brunswick",
    "Newfoundland": "NL - Newfoundland and Labrador | Terre-Neuve-et-Labrador",
    "Nova Scotia": "NS - Nova Scotia | Nouvelle-Écosse",
    "Ontario": "ON - Ontario | Ontario",
    "Prince Edward Island": "PE - Prince Edward Island | Île-du-Prince-Édouard",
    "Quebec": "QC - Quebec | Québec",
    "Saskatchewan": "SK - Saskatchewan | Saskatchewan",
    "Northwest Territories": "NT - Northwest Territories | Territoires du Nord-Ouest",
    "Nunavut": "NU - Nunavut | Nunavut",
    "Yukon": "YT - Yukon | Yukon",
}
regions = {
    "Atlantic": "Atlantic | Atlantique",
    "British Columbia / Yukon": "British Columbia and Yukon | Colombie-Britannique et Yukon",
    "Prairies / Northwest Territories": "Praries and Northwest Territories | Prairies et Territoires du Nord-Ouest",
    "NCR": "NCR | NRC",
    "Ontario": "Ontario | Ontario",
    "Quebec / Nunavut": "Quebec and Nunavut | Québec et Nunavut",
    "International": "International",
}

with (
    open("in/IMFolders CCSP.csv") as f1,
    open("out/PSIMS Workspaces.csv", "w", newline="") as f2,
):
    reader = csv.DictReader(f1)
    fieldnames = ["Workspace Name", "Workspace ID", "Subfolder ID"]
    writer = csv.DictWriter(f2, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        wksp_name = "{} - {} - {}".format(
            row["PSIMS/File #"], row["Project Title"], row["Program"]
        ).replace(":", "")

        response = gcdocs.check_node_name(parent_id=root_id, node_name=wksp_name)

        if response and "results" in response and response["results"]:
            wksp_id = response["results"][0]["id"]
        else:
            category_data = {
                "33223384": {
                    "33223384_5": row["PSIMS/File #"],
                    "33223384_4": row["Project Title"],
                    "33223384_7": provinces[row["Recipient Location"]],
                    "33223384_8": regions[row["PS Regions"]],
                    "33223384_3": row["Funding Type"],
                    "33223384_6": row["Recipient Organization"],
                    "33223384_2": row["Program"],
                    "33223384_9": row["Agreement Status"],
                }
            }
            response = gcdocs.create_workspace(
                workspace_template_id=33223434,
                workspace_name=wksp_name,
                workspace_description="",
                workspace_type=117,
                category_data=category_data,
                parent_id=root_id,
            )
            wksp_id = gcdocs.get_result_value(response=response, key="id")

            if not wksp_id:
                print(wksp_name)
                print("Other error")
                continue

        response = gcdocs.check_node_name(parent_id=wksp_id, node_name="Application")
        folder_id = response["results"][0]["id"]
        response = gcdocs.check_node_name(
            parent_id=folder_id, node_name="Application and required documents"
        )
        subfolder_id = response["results"][0]["id"]
        writer.writerow(
            {
                "Workspace Name": wksp_name,
                "Workspace ID": wksp_id,
                "Subfolder ID": subfolder_id,
            }
        )
