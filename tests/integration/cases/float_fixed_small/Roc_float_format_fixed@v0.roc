module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 0.000000001,
    RFloat -0.000000001,
    ]
