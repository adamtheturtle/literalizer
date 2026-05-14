module [my_data]

Val : [
    RStr Str,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    RStr "apple",
    RStr "banana",
    RStr "cherry",
    ]
