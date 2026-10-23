process = {api = {fetch = function(...) end}}
process.api.fetch({["data"] = "hello"})
process.api.fetch({["data"] = 42})
process.api.fetch({["data"] = true})
