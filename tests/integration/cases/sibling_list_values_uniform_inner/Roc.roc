module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("lint", RList [RInt 2i128, RList [RInt 1i128]]),
    ("test", RList [RInt 5i128, RList [RInt 7i128]]),
    ]
