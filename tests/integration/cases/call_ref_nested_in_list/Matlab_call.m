process = @(varargin) [];
my_var = 42;
my_other = 7;
process({struct('ref', "my_var"), 42, "static"})
process({struct('ref', "my_other"), 7, "label"})
