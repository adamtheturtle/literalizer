module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("vals", RList [RStr "2024-01-15", RStr "09:30:00"]),
    ]
