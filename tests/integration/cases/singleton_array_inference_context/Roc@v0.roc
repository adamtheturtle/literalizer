module [my_data]

Val : [
    RNull,
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("nil", RList [RList [RList [RList [RList [RList [RList [RList [RList [RNull]]]]]]]]]),
    ("empty", RList [RList [RList [RList [RList [RList [RList [RList [RList [RList []]]]]]]]]]),
    ("siblings", RList [RList [RList [RList [RList [RList [RList [RList [RList [RList [RInt 4i128, RInt 5i128]]]]]]]]]]),
]
