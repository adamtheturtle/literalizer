module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RFloat 1.5, RFloat 2.5],
    RList [RFloat 3.5, RFloat 4.5],
    ]
