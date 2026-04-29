module [my_data]

JsonVal : [
    RNull,
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, JsonVal)),
]

my_data : JsonVal
my_data = RDict [
    ("name", RStr "Alice"),
    ("age", RInt 30i128),
    ("active", RBool Bool.true),
    ("score", RNull),
    ]
