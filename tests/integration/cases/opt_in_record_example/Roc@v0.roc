module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Ada"),
    ("active", RBool Bool.true),
    ("scores", RList [RInt 1i128, RInt 2i128, RInt 3i128]),
]
