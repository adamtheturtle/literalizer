process(args...; kwargs...) = nothing
struct TracerType; emit; end
tracer = TracerType((args...; kwargs...) -> nothing)
tracer.emit(process(value="hello"))
tracer.emit(process(value=42))
tracer.emit(process(value=true))
