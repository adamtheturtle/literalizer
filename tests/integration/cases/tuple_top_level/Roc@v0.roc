module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 1i128,
    RStr "email",
    RStr "a@gmail.com",
    RInt 100i128,
    ]
