module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    # line 1
    # line 2
    RStr "a",
    ]
