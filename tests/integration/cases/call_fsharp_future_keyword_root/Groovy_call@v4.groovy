class _ApiType { def fetch(Map _args) { null } }
class _ProcessType { def api = new _ApiType() }
def process = new _ProcessType()
process.api.fetch(data: ["data": "hello"])
process.api.fetch(data: ["data": 42])
process.api.fetch(data: ["data": true])
