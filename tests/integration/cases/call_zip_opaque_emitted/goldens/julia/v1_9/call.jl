using Dates
process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value=1), DateTime(2024, 1, 15, 12, 0, 0))
