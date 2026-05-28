module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 0.0,
    RFloat 1.0,
    RFloat 1.5e3,
    RFloat 1.0e-3,
    RFloat 1.0e16,
    ]
