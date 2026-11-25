using Dates
process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value=1), Date(2024, 1, 15))
