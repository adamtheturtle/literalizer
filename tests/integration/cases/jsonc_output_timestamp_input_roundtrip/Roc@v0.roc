module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # event time
    ("when", RStr "2024-01-15T12:34:56+00:00"),
]
