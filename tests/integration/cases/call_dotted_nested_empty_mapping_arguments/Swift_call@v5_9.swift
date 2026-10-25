class _workerType { @discardableResult func process(values: Any = 0, count: Any = 0) -> Any { 0 } }
class _apiType { var worker = _workerType() }
let api = _apiType()
api.worker.process(values: [1, [String: Any]()], count: 42);
api.worker.process(values: [2, ["x": "s"]], count: 43);
