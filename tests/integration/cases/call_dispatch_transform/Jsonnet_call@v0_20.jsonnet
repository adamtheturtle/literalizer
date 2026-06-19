local record_value(value) = null;
local flush_buffer(count) = null;
local emit(_arg) = null;
[
    emit(record_value(value=42)),
    flush_buffer(count=3),
]
