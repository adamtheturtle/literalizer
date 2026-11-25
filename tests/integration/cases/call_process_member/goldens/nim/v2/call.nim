type ProcessType = object
type AppType = object
    process: ProcessType
template fetch(self: ProcessType; args: varargs[untyped]) = discard
var app: AppType
app.process.fetch({"data": "hello"})
app.process.fetch({"data": 42})
app.process.fetch({"data": true})
