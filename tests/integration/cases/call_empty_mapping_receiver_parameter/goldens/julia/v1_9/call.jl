struct ApiType; process; end
api = ApiType((args...; kwargs...) -> nothing)
api.process(self=Dict())
