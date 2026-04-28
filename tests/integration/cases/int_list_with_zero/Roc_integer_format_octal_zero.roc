module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0o0,
    RInt 0o1,
    RInt -0o1,
    ]
