module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # heading
    ("a", RStr "single ' // data"),
    ("b", RStr "linecontinuation"),
    ("c", RStr "\\"),  # actual comment
    ("d", RStr "  "),  # final comment
]
