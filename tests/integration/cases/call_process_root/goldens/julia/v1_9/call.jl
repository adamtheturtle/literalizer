struct ApiType; fetch; end
struct ProcessType; api; end
process = ProcessType(ApiType((args...; kwargs...) -> nothing))
process.api.fetch(data=Dict("data" => "hello"))
process.api.fetch(data=Dict("data" => 42))
process.api.fetch(data=Dict("data" => true))
