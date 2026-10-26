module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

shared : Val
shared = RList [
    RInt 1i128,
    RStr "x",
]
my_data : Val
my_data = RList [
    shared,
    shared,
]
