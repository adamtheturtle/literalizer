local process(value) = null;
local tracer = { emit(_arg):: null };
[
    tracer.emit(process(value="hello")),
    tracer.emit(process(value=42)),
    tracer.emit(process(value=true)),
]
