module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

shared_var : Val
shared_var = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RList [
    shared_var,
    shared_var,
    ]
