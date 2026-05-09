class AppClient_ {
    construct new() {}
    fetch(value) {}
}
class App_ {
    client { _client }
    construct new() {
        _client = AppClient_.new()
    }
}
var app = App_.new()
app.client.fetch("hello")
app.client.fetch("world")
