module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "100% done",
    RStr "%(name) is here",
    ]
