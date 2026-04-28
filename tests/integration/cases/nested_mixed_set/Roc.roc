module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
    RSet (List Val),
]

my_data : Val
my_data = RDict [
    ("name", RStr "Alice"),
    ("tags", RSet [RBool Bool.true, RInt 42i128, RStr "apple"]),
    ]
