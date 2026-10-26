module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("del", RStr "ab"),
    ("nel", RStr "ab"),
    ("c1", RStr "ab"),
]
