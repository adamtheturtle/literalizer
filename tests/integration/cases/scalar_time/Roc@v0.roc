module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("starts_at", RStr "09:30:00"),
    ]
