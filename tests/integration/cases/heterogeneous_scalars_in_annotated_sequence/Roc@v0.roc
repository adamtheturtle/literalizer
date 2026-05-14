module [my_data]

Val : [
    RNull,
    RBool Bool,
    RFloat F64,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RBool Bool.true,
    RFloat 1.5,
    RNull,
    RStr "2020-01-01",
    RStr "2020-01-01T00:00:00+00:00",
    RList [],
    ]
