module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("date", RStr "2024-01-15"),
    ("datetime", RStr "2024-01-15T12:30:00+00:00"),
    ]
