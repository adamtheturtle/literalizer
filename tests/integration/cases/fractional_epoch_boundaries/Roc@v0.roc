module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "1970-01-01T00:00:00.000001+00:00",
    RStr "1969-12-31T23:59:59.500000+00:00",
    RStr "1970-01-01T00:00:01+00:00",
]
