module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("timestamp", RStr "2020-01-01T00:00:00+00:00")],
    RDict [],
]
