class WorkerType; def process(*a, **kw); end; end
class ApiType; def worker; WorkerType.new; end; end
api = ApiType.new
api.worker.process(values: [1, {}], count: 42)
api.worker.process(values: [2, {"x" => "s"}], count: 43)
