module [my_data]

Val : [
    JStr Str,
    JDict (List (Str, Val)),
]

my_data : Val
my_data = JDict [
    ("date", JStr "0099-05-27"),
    ("naive", JStr "0001-01-01T12:30:00"),
    ("recent", JStr "2024-05-27T10:00:00"),
]
