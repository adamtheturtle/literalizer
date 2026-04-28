process = @(varargin) [];
log.emit = @(varargin) [];
log.emit(process("hello"))
log.emit(process(42))
log.emit(process(true))
