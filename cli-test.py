from json_server_client import JsonClient
c = JsonClient(8080)
res = c.get_successors({ "words": ["нешто", "што"] })
print(res)

# for _ in range(100000):
#     res = c.send_request({ "method": "get_successors", "params": { "words": ["зборови"] } })
#     # print(res)
