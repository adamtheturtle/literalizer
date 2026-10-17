class AppClient_ {
    construct new() {}
    go(first_value, second_value) {}
}
class App_ {
    client { _client }
    construct new() {
        _client = AppClient_.new()
    }
}
var app = App_.new()
app.client.go([1], [2])
