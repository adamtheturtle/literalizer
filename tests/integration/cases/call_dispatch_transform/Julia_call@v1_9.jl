record_value(args...; kwargs...) = nothing
flush_buffer(args...; kwargs...) = nothing
emit(args...; kwargs...) = nothing
emit(record_value(value=42))
flush_buffer(count=3)
