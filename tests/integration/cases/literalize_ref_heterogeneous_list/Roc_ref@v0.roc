module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

one : Val
one = RInt 1i128
two : Val
two = RStr "s"
my_data : Val
my_data = RList [
    one,
    two,
]
