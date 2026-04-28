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
    RInt 1,
    RStr "hello",
    RBool Bool.true,
    RNull,
    ]
