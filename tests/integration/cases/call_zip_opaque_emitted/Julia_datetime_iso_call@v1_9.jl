process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value=1), "2024-01-15T12:00:00")
