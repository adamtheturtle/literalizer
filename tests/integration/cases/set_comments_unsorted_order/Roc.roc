module [my_data]

Val : [
    RStr Str,
    RSet (List Val),
]

my_data : Val
my_data = RSet [
    # before apple
    RStr "apple",
    RStr "banana",  # banana inline
    # trailing
    ]
