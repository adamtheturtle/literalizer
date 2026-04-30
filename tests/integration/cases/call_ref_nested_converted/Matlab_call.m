process = @(varargin) [];
myVar = 42;
process({struct('ref', "myVar"), 42, "static"})
