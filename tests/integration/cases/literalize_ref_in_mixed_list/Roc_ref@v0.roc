module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

ref_x : Val
ref_x = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RList [
    ref_x,
    RInt 1i128,
    RInt 2i128,
    ]
