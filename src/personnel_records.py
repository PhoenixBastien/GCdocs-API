from threading import Thread

from config import gcdocs
from gcdocs import GCdocs


def assign_workspace_permissions(gcdocs: GCdocs, workspace_id: int) -> None:
    assignees = [
        78209,
        30665104,
        30665384,
        30665444,
        30665659,
        30716420,
        30716726,
        40359816,
        46040346,
        51315755,
    ]

    for assignee in assignees:
        gcdocs.assign_permission(
            node_id=workspace_id,
            permissions=GCdocs.PERMISSION_TYPES[:2],
            assignee_type="custom",
            assignee=assignee,
        )


def assign_subfolder_permissions(gcdocs: GCdocs, workspace_id: int) -> None:
    subfolders = [
        {"name": "AWARDS AND RECOGNITION", "assignees": [30716726]},
        {"name": "COMPENSATION", "assignees": [30665444, 40359816]},
        {"name": "CONFLICT OF INTEREST", "assignees": [30665659]},
        {"name": "DUTY TO ACCOMMODATE", "assignees": [51315755]},
        {"name": "EX PROGRAMS", "assignees": [30716420, 30665444]},
        {"name": "LABOUR RELATIONS", "assignees": [30665384]},
        {"name": "LEARNING AND DEVELOPMENT", "assignees": [30716726]},
        {"name": "OCCUPATIONAL HEALTH AND SAFETY", "assignees": [78209]},
        {"name": "STAFFING", "assignees": [30665104, 30665444]},
    ]

    for node in subfolders:
        node_name = node["name"]
        assignees = node["assignees"]
        response = gcdocs.check_node_name(parent_id=workspace_id, node_name=node_name)

        if response and "results" in response and response["results"]:
            node_id = response["results"][0]["id"]
        else:
            response = gcdocs.create_item(
                parent_id=workspace_id,
                item_type=GCdocs.ITEM_TYPE_FOLDER,
                item_name=node_name,
            )
            node_id = gcdocs.get_result_value(response=response, key="id")

        for assignee in assignees:
            response = gcdocs.assign_permission(
                node_id=node_id,
                permissions=GCdocs.PERMISSION_TYPES[:6],
                assignee_type="custom",
                assignee=assignee,
                apply_to=2,
            )


def personnel_records(gcdocs: GCdocs, workspaced_id: int) -> None:
    gcdocs.clear_workspace_roles(workspace_id=workspaced_id)
    assign_workspace_permissions(gcdocs=gcdocs, workspace_id=workspaced_id)
    assign_subfolder_permissions(gcdocs=gcdocs, workspace_id=workspaced_id)


root_id = 30713183
page_size = 100

root = gcdocs.get_node(node_id=root_id)
total_subnodes = gcdocs.get_result_value(response=root, key="size")
total_pages = (total_subnodes + page_size - 1) // page_size

for page in range(1, total_pages + 1):
    print(f"page {page}/{total_pages}")
    nodes = gcdocs.get_subnodes(
        parent_node_id=root_id,
        filter_node_types=GCdocs.ITEM_TYPE_BUSINESS_WORKSPACE,
        limit=page_size,
        page=page,
    )
    node_ids = gcdocs.get_result_values(response=nodes, key="id")
    threads: list[Thread] = []

    for node_id in node_ids:
        threads.append(
            Thread(
                target=gcdocs.assign_permission,
                args=(node_id, GCdocs.PERMISSION_TYPES, "custom", 31897943, 2),
            )
        )

    for t in threads:
        t.start()

    for t in threads:
        t.join()
