module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a-b", RInt 1i128),
    ("two words", RInt 2i128),
    ("she said \"hi\"", RInt 3i128),
    ("", RInt 4i128),
    ("valid_key", RInt 5i128),
]
