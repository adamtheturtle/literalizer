app = {process = {fetch = function(...) end}}
app.process.fetch({["data"] = "hello"})
app.process.fetch({["data"] = 42})
app.process.fetch({["data"] = true})
