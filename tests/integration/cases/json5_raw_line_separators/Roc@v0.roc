module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("double", RStr "a b"),
    ("single", RStr "c d"),
    # A comment, which both separators would end.
    ("both", RStr "e f g"),
    ("continued", RStr "hi"),
    ("escaped backslash", RStr "j\\ k"),
]
