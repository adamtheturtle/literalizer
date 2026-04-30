process(args...; kwargs...) = nothing
my_var = 42
process(data=Dict("key" => Dict("ref" => "my_var"), "count" => 42))
