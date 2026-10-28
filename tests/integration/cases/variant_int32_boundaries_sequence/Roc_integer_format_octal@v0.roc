module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt -0o20000000000i128,
    RInt -0o17777777777i128,
    RList [RInt 0o0i128],
]
