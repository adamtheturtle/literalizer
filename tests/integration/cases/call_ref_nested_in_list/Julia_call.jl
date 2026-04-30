process(args...; kwargs...) = nothing
my_var = 42
my_other = 7
process(data=[Dict("ref" => "my_var"), 42, "static"])
process(data=[Dict("ref" => "my_other"), 7, "label"])
