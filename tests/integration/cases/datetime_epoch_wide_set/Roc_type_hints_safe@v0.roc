module [my_data]

Val : [
    RStr Str,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RStr "2099-06-15T08:30:00",
]
