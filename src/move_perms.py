from config import gcdocs

node_id = 52738856
old_parent_id = 33751816
new_parent_id = 34421547

old_rm = gcdocs.get_node_classifications(node_id=node_id)
old_cats = gcdocs.get_node_categories(node_id=node_id)
old_perms = gcdocs.get_node_permissions(node_id=node_id)
print(
    gcdocs.get_result_values(
        response=old_perms, key="right_id", property_name="permissions"
    )
)
gcdocs.update_item(node_id=node_id, parent_id=new_parent_id)

new_rm = gcdocs.get_node_classifications(node_id=node_id)
new_cats = gcdocs.get_node_categories(node_id=node_id)
new_perms = gcdocs.get_node_permissions(node_id=node_id)
print(
    gcdocs.get_result_values(
        response=new_perms, key="right_id", property_name="permissions"
    )
)
gcdocs.update_item(node_id=node_id, parent_id=old_parent_id)

print(old_perms == new_perms)
