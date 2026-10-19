module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1i128,
    RStr "a",
    RFloat 2.5,
]
