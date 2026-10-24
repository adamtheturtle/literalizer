module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -0b101010i128,
    RInt 0b0i128,
    RInt 0b101010i128,
    RFloat -1.25,
    RFloat 0.0,
    RFloat 1.25,
]
