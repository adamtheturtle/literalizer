module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "1901-12-13T20:45:51",
    RStr "1901-12-13T20:45:52",
    RStr "2038-01-19T03:14:07",
    RStr "2038-01-19T03:14:08",
]
