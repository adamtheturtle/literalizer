module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("url", RStr "https://example.org/a/*b*/"),
    ("count", RInt 2i128),
]
