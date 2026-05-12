module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RBool Bool.true,
    RInt 42i128,
    RStr "apple",
    ]
