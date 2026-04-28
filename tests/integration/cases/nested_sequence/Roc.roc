module [my_data]

Val : [
    RNull,
    RBool Bool,
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RBool Bool.true,
    RStr "hi",
    RList [RInt 1, RInt 2],
    RNull,
    ]
