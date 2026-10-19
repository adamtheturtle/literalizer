module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -42i128,
    RInt 0i128,
    RInt 42i128,
    RFloat -1.250000,
    RFloat 0.000000,
    RFloat 1.250000,
]
