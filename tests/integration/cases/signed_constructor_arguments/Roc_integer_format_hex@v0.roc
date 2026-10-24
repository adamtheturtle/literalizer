module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -0x2ai128,
    RInt 0x0i128,
    RInt 0x2ai128,
    RFloat -1.25,
    RFloat 0.0,
    RFloat 1.25,
]
