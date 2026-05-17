module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("exact_millisecond", RStr "09:30:15.123000"),
    ("sub_millisecond", RStr "09:30:15.123456"),
    ]
