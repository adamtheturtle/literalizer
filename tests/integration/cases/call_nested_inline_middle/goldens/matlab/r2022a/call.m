f = @(varargin) [];
f({{"DEL", "b", "10"}, {"ADD", "a", "x"}})  % note
% next call
f({{"ADD", "c", "y"}})
