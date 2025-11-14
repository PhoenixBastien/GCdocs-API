import pandas as pd

from config import gcdocs

node_id = 33751816
nodes = gcdocs.get_subnodes(parent_node_id=node_id)
df = pd.DataFrame.from_dict([node["data"]["properties"] for node in nodes["results"]])
df.to_excel("out/items_info.xlsx", index=False)
