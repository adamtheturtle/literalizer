module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 42i128,
    RFloat 3.14,
    RBool Bool.true,
    RBool Bool.false,
    RStr "hello \"world\"",
    ]
