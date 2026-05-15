local process(value) = null;
local emit(_call, _zip) = null;
[
    emit(process(value="hello"), true),
    emit(process(value=42), false),
]
