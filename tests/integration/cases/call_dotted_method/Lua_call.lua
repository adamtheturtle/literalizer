app = {client = {fetch = function(...) end}}
app.client.fetch("hello")
app.client.fetch(42)
app.client.fetch(true)
