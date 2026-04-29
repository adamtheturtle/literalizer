process = @(varargin) [];
tracer.emit = @(varargin) [];
tracer.emit(process("hello"))
tracer.emit(process(42))
tracer.emit(process(true))
