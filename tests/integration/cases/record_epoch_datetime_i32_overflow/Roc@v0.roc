module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("within_i32", RStr "2024-01-15T12:00:00"),
    ("beyond_i32", RStr "2099-06-15T08:30:00"),
    ]
