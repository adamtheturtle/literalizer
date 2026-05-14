module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "2024-01-15",
    RStr "2024-02-20",
    ]
