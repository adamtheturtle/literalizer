module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    RDict [("timestamp", RStr "2040-01-01T03:00:00+03:00")],
    RDict [],
]
