local process(value) = null;
local emit(_call, _zip) = null;
[
    emit(process(value="hello"), 1),
    emit(process(value=42), 0),
]
