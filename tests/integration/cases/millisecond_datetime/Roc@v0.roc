module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("half", RStr "1979-05-27T07:32:00.500000"),
    ("milli", RStr "1979-05-27T07:32:00.100000"),
    ("max_milli", RStr "1979-05-27T07:32:00.999000"),
    ("whole", RStr "1979-05-27T07:32:00"),
]
