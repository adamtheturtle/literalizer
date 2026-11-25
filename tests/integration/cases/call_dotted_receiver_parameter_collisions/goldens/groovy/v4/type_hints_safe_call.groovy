class _WorkerType { def process(Map _args) { null } }
class _ApiType { def worker = new _WorkerType() }
def api = new _ApiType()
api.worker.process(self: [:], self_: [:])
