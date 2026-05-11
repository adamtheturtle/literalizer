module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "hello",
    RInt 42i128,
    ]
