process(args...; kwargs...) = nothing
struct LogType; emit; end
log = LogType((args...; kwargs...) -> nothing)
log.emit(process(value="hello"))
log.emit(process(value=42))
log.emit(process(value=true))
