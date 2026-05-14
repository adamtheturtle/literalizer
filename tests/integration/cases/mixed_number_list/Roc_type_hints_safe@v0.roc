module [my_data]

Val : [
    RInt I128,
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1i128,
    RFloat 2.5,
    RInt 3i128,
    ]
