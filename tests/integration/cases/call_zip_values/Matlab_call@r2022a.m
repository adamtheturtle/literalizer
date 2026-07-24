process = @(varargin) [];
emit = @(varargin) [];
emit(process("hello"), 1)
emit(process(42), 0)
