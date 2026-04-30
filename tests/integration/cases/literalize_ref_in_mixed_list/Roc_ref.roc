module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

x : Val
x = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RList [
    x,
    RInt 1i128,
    RInt 2i128,
    ]
