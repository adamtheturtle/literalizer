obj = {api = {client = {post = function(...) end}}}
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(true)
