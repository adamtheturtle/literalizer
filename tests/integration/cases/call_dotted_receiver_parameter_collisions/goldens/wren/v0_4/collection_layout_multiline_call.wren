class ApiWorker_ {
    construct new() {}
    process(self, self_) {}
}
class Api_ {
    worker { _worker }
    construct new() {
        _worker = ApiWorker_.new()
    }
}
var api = Api_.new()
api.worker.process({}, {})
