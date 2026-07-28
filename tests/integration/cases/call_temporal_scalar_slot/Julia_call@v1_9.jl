using Dates
process(args...; kwargs...) = nothing
process(value="09:30:00")
process(value=DateTime(2024, 1, 15, 0, 0, 0))
process(value=1)
