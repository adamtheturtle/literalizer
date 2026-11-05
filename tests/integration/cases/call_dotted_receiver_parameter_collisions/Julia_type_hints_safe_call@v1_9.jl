struct WorkerType; process; end
struct ApiType; worker; end
api = ApiType(WorkerType((args...; kwargs...) -> nothing))
api.worker.process(self=Dict(), self_=Dict())
