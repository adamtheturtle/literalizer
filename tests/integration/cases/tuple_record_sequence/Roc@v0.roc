module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("call", RStr "send"), ("args", RList [RInt 1i128, RStr "email", RStr "a@gmail.com", RInt 100i128])],
    RDict [("call", RStr "recv"), ("args", RList [RInt 2i128, RStr "sms", RStr "b@example.com", RInt 200i128])],
    ]
