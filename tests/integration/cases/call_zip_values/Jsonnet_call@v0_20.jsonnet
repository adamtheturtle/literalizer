local process(value) = null;
local emit(_call, _zip) = null;
[
    emit(process(value="hello"), "one"),
    emit(process(value=42), "zero"),
]
