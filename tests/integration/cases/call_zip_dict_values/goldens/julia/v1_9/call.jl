process(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(process(value="hello"), Dict("a" => 1, "b" => 2))
emit(process(value=42), Dict("c" => 3, "d" => 4))
