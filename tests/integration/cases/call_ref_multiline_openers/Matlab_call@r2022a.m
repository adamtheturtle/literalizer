consume = @(varargin) [];
foo = 42;
consume({
    struct(
        'other', 1
    ),
    foo
}, struct(
    'left', foo,
    'other', 1
))
