module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 0.000000,
    RFloat 1.000000,
    RFloat 1500.000000,
    RFloat 0.001000,
    RFloat 10000000000000000.000000,
    ]
