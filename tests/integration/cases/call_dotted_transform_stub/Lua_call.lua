function process(...) end
log = {emit = function(...) end}
log.emit(process("hello"))
log.emit(process(42))
log.emit(process(true))
