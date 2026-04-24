process(args...; kwargs...) = nothing
my_var = [
    1,
    2,
    3,
]
my_other = [
    4,
    5,
    6,
]
process(data=my_var, count=42)
process(data=my_other, count=7)
