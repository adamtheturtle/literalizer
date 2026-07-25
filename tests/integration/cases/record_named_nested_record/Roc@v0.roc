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
    ("collection", RStr "alpha"),
    ("featured_entry", RDict [("id", RInt 100i128), ("label", RStr "first entry"), ("enabled", RBool Bool.false), ("related_ids", RList [RInt 102i128, RInt 103i128])]),
    ]
