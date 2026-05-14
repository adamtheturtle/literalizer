module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 1.100000,
    RFloat -2.200000,
    RFloat 3.300000,
    ]
