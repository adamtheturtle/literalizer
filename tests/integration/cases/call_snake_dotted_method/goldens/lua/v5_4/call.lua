my_app = {http_client = {fetch = function(...) end}}
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(true)
