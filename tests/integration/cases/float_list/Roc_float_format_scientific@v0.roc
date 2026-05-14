module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 1.1,
    RFloat -2.2,
    RFloat 3.3,
    ]
