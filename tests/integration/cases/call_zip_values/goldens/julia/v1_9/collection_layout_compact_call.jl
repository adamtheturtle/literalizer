process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value="hello"), true)
emit(process(value=42), false)
