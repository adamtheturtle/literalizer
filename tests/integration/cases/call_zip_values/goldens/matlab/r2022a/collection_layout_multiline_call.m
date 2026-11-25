process = @(varargin) [];
emit = @(varargin) [];
emit(process("hello"), true)
emit(process(42), false)
