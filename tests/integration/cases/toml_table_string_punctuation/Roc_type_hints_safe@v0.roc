module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("comma_hash", RStr "a,#b"),
    ("comma_space_hash", RStr "trail, # comment"),
    ("escaped_quote", RStr "quote \" and , #"),
    ("next_line", RStr "xy"),
    ("line_separator", RStr "x y"),
    ("paragraph_separator", RStr "x y"),
]
