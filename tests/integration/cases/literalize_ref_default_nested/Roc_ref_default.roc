module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

item_var : Val
item_var = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RDict [
    ("items", RList [item_var, RDict [("fallback", RStr "value")]]),
    ]
