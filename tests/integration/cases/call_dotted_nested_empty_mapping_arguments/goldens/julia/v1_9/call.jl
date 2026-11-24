struct WorkerType; process; end
struct ApiType; worker; end
api = ApiType(WorkerType((args...; kwargs...) -> nothing))
api.worker.process(values=[1, Dict()], count=42)
api.worker.process(values=[2, Dict("x" => "s")], count=43)
