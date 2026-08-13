module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "]",
    RStr "a]",
    RStr "a]=",
    RStr "a]b",
    ]
