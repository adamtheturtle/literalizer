type ApiType = object
type ProcessType = object
    api: ApiType
template fetch(self: ApiType; args: varargs[untyped]) = discard
var process: ProcessType
process.api.fetch({"data": "hello"})
process.api.fetch({"data": 42})
process.api.fetch({"data": true})
