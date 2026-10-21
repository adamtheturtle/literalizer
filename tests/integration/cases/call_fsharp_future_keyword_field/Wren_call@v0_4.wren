class AppProcess_ {
    construct new() {}
    fetch(data) {}
}
class App_ {
    process { _process }
    construct new() {
        _process = AppProcess_.new()
    }
}
var app = App_.new()
app.process.fetch({"data": "hello"})
app.process.fetch({"data": 42})
app.process.fetch({"data": true})
