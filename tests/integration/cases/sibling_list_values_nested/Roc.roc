module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("lint", RList [RInt 2, RList []]),
    ("test", RList [RInt 5, RList [RStr "compile"]]),
    ]
