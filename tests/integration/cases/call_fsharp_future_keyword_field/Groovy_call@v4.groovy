class _ProcessType { def fetch(Map _args) { null } }
class _AppType { def process = new _ProcessType() }
def app = new _AppType()
app.process.fetch(data: ["data": "hello"])
app.process.fetch(data: ["data": 42])
app.process.fetch(data: ["data": true])
