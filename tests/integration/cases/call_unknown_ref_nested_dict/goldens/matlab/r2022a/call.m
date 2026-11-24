process = @(varargin) [];
my_list = struct(
    'unused', "value"
);
process({{struct('inner', my_list)}})
