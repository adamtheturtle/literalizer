client = {api = {request = function(...) end}}
client.api.request("hello")
client.api.request(42)
client.api.request(true)
