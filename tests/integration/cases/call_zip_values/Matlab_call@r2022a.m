process = @(varargin) [];
emit = @(varargin) [];
emit(process("hello"), "one")
emit(process(42), "zero")
