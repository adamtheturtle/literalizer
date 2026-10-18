module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "2020-06-15T12:00:00-23:59",
    RStr "2020-06-15T12:00:00-18:00",
    RStr "2020-06-15T12:00:00+18:00",
    RStr "2020-06-15T12:00:00+23:59",
]
