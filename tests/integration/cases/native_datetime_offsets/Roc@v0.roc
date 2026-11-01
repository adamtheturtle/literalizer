module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("stamps", RList [RStr "2001-02-03T04:05:06+00:00:01", RStr "2001-02-03T04:05:06-00:00:01", RStr "2001-02-03T04:05:06+00:00:00.000001", RStr "2001-02-03T04:05:06-00:00:00.000001", RStr "2001-02-03T04:05:06+05:30:15.000001", RStr "2001-02-03T04:05:06-05:30:15.000001"]),
]
