module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 1.0e-9,
    RFloat -1.0e-9,
    ]
