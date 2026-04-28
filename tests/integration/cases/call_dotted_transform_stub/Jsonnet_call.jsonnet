local process(value) = null;
local log = { emit(_arg):: null };
[
    log.emit(process(value="hello")),
    log.emit(process(value=42)),
    log.emit(process(value=true)),
]
