process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value="hello"), "one")
emit(process(value=42), "zero")
