class _WorkerType { def process(Map _args) { null } }
class _ApiType { def worker = new _WorkerType() }
def api = new _ApiType()
api.worker.process(values: [1, [:]], count: 42)
api.worker.process(values: [2, ["x": "s"]], count: 43)
