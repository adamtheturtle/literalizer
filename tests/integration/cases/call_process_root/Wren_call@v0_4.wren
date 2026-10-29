class ProcessApi_ {
    construct new() {}
    fetch(data) {}
}
class Process_ {
    api { _api }
    construct new() {
        _api = ProcessApi_.new()
    }
}
var process = Process_.new()
process.api.fetch({"data": "hello"})
process.api.fetch({"data": 42})
process.api.fetch({"data": true})
