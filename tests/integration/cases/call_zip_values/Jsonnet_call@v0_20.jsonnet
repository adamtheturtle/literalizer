local process(value) = null;
local emit(_call, _zip) = null;
[
    emit(_call=process(value="hello"), _zip=true),
    emit(_call=process(value=42), _zip=false),
]
