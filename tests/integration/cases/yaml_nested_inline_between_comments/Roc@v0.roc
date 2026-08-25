module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RInt 2i128, RStr "hello"],  # trailing note
    # next element
    RList [RInt 3i128, RStr "world"],
    ]
