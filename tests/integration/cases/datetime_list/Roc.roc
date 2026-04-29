module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "2024-01-15T12:30:00.123456+00:00",
    RStr "2024-06-01T08:00:00+00:00",
    ]
