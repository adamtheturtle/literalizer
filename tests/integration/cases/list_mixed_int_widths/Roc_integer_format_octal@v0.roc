module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 0o1i128,
    RInt 0o20000000000000i128,
]
