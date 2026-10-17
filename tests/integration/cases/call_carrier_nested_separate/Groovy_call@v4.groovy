class _ClientType { def go(Map _args) { null } }
class _AppType { def client = new _ClientType() }
def app = new _AppType()
app.client.go(first_value: [1], second_value: ["text"])
