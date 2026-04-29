module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    # first
    RStr "a",
    # second
    RStr "b",
    ]
