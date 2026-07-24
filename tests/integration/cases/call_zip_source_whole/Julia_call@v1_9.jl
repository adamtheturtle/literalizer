process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value=42), 1)
