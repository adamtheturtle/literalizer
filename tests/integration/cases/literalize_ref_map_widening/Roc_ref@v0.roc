module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

string_map : Val
string_map = RDict [
    ("k", RStr "s"),
]
my_data : Val
my_data = RList [
    string_map,
    RDict [("k", RInt 1i128)],
]
