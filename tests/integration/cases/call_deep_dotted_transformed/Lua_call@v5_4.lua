app = {client = {fetch = function(...) end}}
function emit(...) end
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
