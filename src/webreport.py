from io import StringIO

import pandas as pd

from config import gcdocs

node_id = 46434215
request_url = gcdocs.config()["nodesUrl"] + "/" + str(node_id) + "/output"
request_header = gcdocs.request_form_header()

response = gcdocs.do_request(
    url=request_url,
    method="GET",
    headers=request_header,
    timeout=None,
    failure_message="Failed to get WebReport output",
)

data = response["data"]
df = pd.read_html(StringIO(data))[0]
df.to_excel("out/WebReport Output.xlsx", index=False)
