process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value="hello"), 1)
emit(process(value=42), 0)
