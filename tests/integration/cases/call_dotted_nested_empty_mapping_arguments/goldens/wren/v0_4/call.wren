class ApiWorker_ {
    construct new() {}
    process(values, count) {}
}
class Api_ {
    worker { _worker }
    construct new() {
        _worker = ApiWorker_.new()
    }
}
var api = Api_.new()
api.worker.process([1, {}], 42)
api.worker.process([2, {"x": "s"}], 43)
