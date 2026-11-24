struct ProcessType; fetch; end
struct AppType; process; end
app = AppType(ProcessType((args...; kwargs...) -> nothing))
app.process.fetch(data=Dict("data" => "hello"))
app.process.fetch(data=Dict("data" => 42))
app.process.fetch(data=Dict("data" => true))
