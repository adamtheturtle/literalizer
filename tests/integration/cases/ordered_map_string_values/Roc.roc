module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("first", RStr "one"),
    ("second", RStr "two"),
    ("third", RStr "three"),
    ]
