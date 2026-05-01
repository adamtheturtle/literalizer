module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_var : Val
my_var = RDict [
    ("_", RStr "_"),
    ]
item_var : Val
item_var = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RDict [
    ("key", my_var),
    ("items", RList [item_var, RDict [("fallback", RStr "value")]]),
    ]
