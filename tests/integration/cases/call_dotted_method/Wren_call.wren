class AppClient_ {
    fetch(payload) {}
}
class App_ {
    client { _client }
    construct new() {
        _client = AppClient_.new()
    }
}
var app = App_.new()
app.client.fetch("hello")
app.client.fetch(42)
app.client.fetch(true)
