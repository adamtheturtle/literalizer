module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

shared : Val
shared = RList [
    RList [RInt 1i128, RInt 2i128],
    RDict [("value", RInt 1i128)],
]
my_data : Val
my_data = RList [
    shared,
    shared,
]
