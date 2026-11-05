process = @(varargin) [];
emit = @(varargin) [];
emit(process("hello"), struct('a', 1, 'b', 2))
emit(process(42), struct('c', 3, 'd', 4))
