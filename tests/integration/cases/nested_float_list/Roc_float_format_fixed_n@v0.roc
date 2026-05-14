module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RFloat 1.500000, RFloat 2.500000],
    RList [RFloat 3.500000, RFloat 4.500000],
    ]
