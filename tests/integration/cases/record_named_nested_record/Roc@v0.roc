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
    ("project", RStr "alpha"),
    ("lead_task", RDict [("id", RInt 100i128), ("description", RStr "first task"), ("is_done", RBool Bool.false), ("blocks", RList [RInt 102i128, RInt 103i128])]),
    ]
