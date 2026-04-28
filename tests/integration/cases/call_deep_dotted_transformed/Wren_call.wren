class AppClient_ {
    construct new() {}
    fetch(payload) {}
}
class App_ {
    client { _client }
    construct new() {
        _client = AppClient_.new()
    }
}
var app = App_.new()
class Emit_ {
    construct new() {}
    call(arg) {}
}
var emit = Emit_.new()
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
