module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("date", RStr "0099-05-27"),
    ("naive", RStr "0001-01-01T12:30:00"),
    ("recent", RStr "2024-05-27T10:00:00"),
]
